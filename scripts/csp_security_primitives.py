"""Offline input-boundary checks for CSP examples and bounded test fixtures.

Not a chain resolver, secure HTTP fetcher, DAG verifier, or proof verifier.
"""
from __future__ import annotations
import ipaddress
import json
import math
import re
from urllib.parse import urlsplit

REGISTRY = re.compile(r"^eip155:([1-9][0-9]*):(0x[0-9a-f]{40})$")
TOKEN = re.compile(r"^(0|[1-9][0-9]*)$")

def parse_evm_subject(registry: str, token: str) -> tuple[int, str, int]:
    if not isinstance(registry, str) or not isinstance(token, str):
        raise ValueError("subject fields must be strings")
    match = REGISTRY.fullmatch(registry)
    if not match or not TOKEN.fullmatch(token):
        raise ValueError("non-canonical ERC-8004 EVM subject")
    # Preserve integer precision; don't pass subject identifiers through floats.
    chain = int(match.group(1))
    agent_id = int(token)
    if chain.bit_length() > 256 or agent_id.bit_length() > 256:
        raise ValueError("identifier exceeds uint256")
    return chain, match.group(2), agent_id

def strict_json_bytes(data: bytes, max_bytes: int = 65536, max_depth: int = 32) -> object:
    if len(data) > max_bytes:
        raise ValueError("JSON payload exceeds configured byte limit")
    text = data.decode("utf-8", errors="strict")
    if text.startswith("\ufeff"):
        raise ValueError("I-JSON disallows leading BOM")
    def unique_pairs(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError(f"duplicate JSON key: {key}")
            value[key] = item
        return value
    def reject_constant(token):
        raise ValueError(f"non-finite numeric token: {token}")
    parsed = json.loads(text, object_pairs_hook=unique_pairs, parse_constant=reject_constant)
    def depth(value, current):
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError("non-finite JSON numeric value")
        if isinstance(value, str) and any(0xD800 <= ord(c) <= 0xDFFF for c in value):
            raise ValueError("unpaired UTF-16 surrogate in JSON")
        if current > max_depth:
            raise ValueError("JSON nesting too deep")
        if isinstance(value, dict):
            if len(value) > 10000:
                raise ValueError("too many object fields")
            for key, item in value.items():
                depth(key, current+1)
                depth(item, current+1)
        elif isinstance(value, list):
            if len(value) > 10000:
                raise ValueError("too many array elements")
            for item in value:
                depth(item, current+1)
    depth(parsed, 0)
    return parsed

def is_safe_https_literal(url: str) -> bool:
    """Conservative preflight *only*: real fetch MUST validate DNS and connect-time IP."""
    try:
        parsed = urlsplit(url)
        if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
            return False
        if parsed.port not in (None, 443):
            return False
        hostname = parsed.hostname
        if "%" in hostname:  # reject zone IDs
            return False
        try:
            ip = ipaddress.ip_address(hostname)
        except ValueError:
            # Reject ambiguous IPv4 notations sometimes resolved as numeric addresses
            # by legacy clients (127.1, 0177.0.0.1, hex labels etc).
            labels = hostname.lower().split(".")
            if all(label.isdigit() for label in labels):
                return False
            if any(label.startswith("0x") for label in labels):
                return False
            # Hostnames still REQUIRE DNS rebinding and connect-time destination checks.
            return bool(re.fullmatch(r"[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+", hostname))
        if isinstance(ip, ipaddress.IPv6Address):
            if ip.ipv4_mapped is not None or ip.sixtofour is not None or ip.teredo is not None:
                return False
            if ip in ipaddress.ip_network("64:ff9b::/96"):
                return False
        return ip.is_global
    except ValueError:
        return False
