# scripts/demo_generate.py
"""
Demo generator client that calls the running Linda API.

Usage:
    python scripts/demo_generate.py --host http://localhost:8000

This file sends a JSON payload to /v1/generate and prints the response.
"""
import argparse
import requests
import json
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="http://localhost:8000", help="API host (including http:// and port)")
    parser.add_argument("--brand", default="brand_x", help="Brand id")
    parser.add_argument("--channel", default="facebook", help="Channel")
    parser.add_argument("--seed", default="camera battery", help="Seed text or query")
    parser.add_argument("--max_variants", type=int, default=3, help="Max variants")
    args = parser.parse_args()

    url = args.host.rstrip("/") + "/v1/generate"
    payload = {
        "brand_id": args.brand,
        "channel": args.channel,
        "persona": "young_professional",
        "objective": "awareness",
        "seed_text": args.seed,
        "max_variants": args.max_variants,
    }

    print("Sending request to:", url)
    try:
        res = requests.post(url, json=payload, timeout=30)
    except requests.exceptions.RequestException as e:
        print("Failed to call API:", e)
        sys.exit(1)

    print("Status code:", res.status_code)
    try:
        data = res.json()
    except Exception:
        print("Response is not JSON. Raw text:")
        print(res.text)
        sys.exit(1)

    # Pretty print JSON response
    print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
