#!/usr/bin/env python3
"""Manage user consent for privacy policy and third-party disclaimer."""

import json
import os
import sys
import time

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
CONSENT_FILE = os.path.join(DATA_DIR, "consent.json")


def load_consent() -> dict:
    if os.path.exists(CONSENT_FILE):
        with open(CONSENT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_consent(data: dict):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(CONSENT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def check_consent(consent_type: str) -> bool:
    """Check if user has given specific consent."""
    consent = load_consent()
    return consent.get(consent_type, {}).get("accepted", False)


def record_consent(consent_type: str, accepted: bool):
    """Record user's consent decision."""
    consent = load_consent()
    consent[consent_type] = {
        "accepted": accepted,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "version": "2026-04-04",
    }
    save_consent(consent)


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: consent_manager.py <command> [args]"}))
        print("Commands: check <type> | accept <type> | decline <type> | status")
        sys.exit(1)

    command = sys.argv[1]

    if command == "check":
        consent_type = sys.argv[2] if len(sys.argv) > 2 else "privacy_policy"
        result = check_consent(consent_type)
        print(json.dumps({"type": consent_type, "accepted": result}))

    elif command == "accept":
        consent_type = sys.argv[2] if len(sys.argv) > 2 else "privacy_policy"
        record_consent(consent_type, True)
        print(json.dumps({"status": "ok", "type": consent_type, "accepted": True}))

    elif command == "decline":
        consent_type = sys.argv[2] if len(sys.argv) > 2 else "privacy_policy"
        record_consent(consent_type, False)
        print(json.dumps({"status": "ok", "type": consent_type, "accepted": False}))

    elif command == "status":
        consent = load_consent()
        print(json.dumps(consent, ensure_ascii=False))

    else:
        print(json.dumps({"error": f"Unknown command: {command}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
