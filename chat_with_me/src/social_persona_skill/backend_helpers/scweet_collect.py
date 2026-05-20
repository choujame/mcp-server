"""
X / Twitter collection helper — runs inside the Scweet venv.
Usage:
  python scweet_collect.py collect --url=https://x.com/karpathy --token=<auth_token> --db=<path>
Output: JSON array of post dicts to stdout.
"""
from __future__ import annotations
import argparse
import json
import sys
import os
import re


def _username_from_url(url: str) -> str:
    url = url.rstrip("/")
    match = re.search(r"(?:twitter|x)\.com/@?([^/?#]+)", url)
    if match:
        return match.group(1)
    return url.split("/")[-1].lstrip("@")


def collect(url: str, token: str, db: str) -> list:
    try:
        from Scweet.scweet import scrape
    except ImportError:
        print("[scweet] Scweet not installed. Run: backend bootstrap x", file=sys.stderr)
        return []

    username = _username_from_url(url)
    os.environ["auth_token"] = token

    try:
        data = scrape(
            users=[username],
            since="2020-01-01",
            save_images=False,
            resume=db,
        )
        if data is None:
            return []
        if hasattr(data, "to_dict"):
            records = data.to_dict(orient="records")
        else:
            records = list(data)
        return records
    except Exception as e:
        print(f"[scweet] Error collecting {username}: {e}", file=sys.stderr)
        return []


def main():
    parser = argparse.ArgumentParser(
        description="Collect tweets from a user's timeline using Scweet"
    )
    sub = parser.add_subparsers(dest="cmd")
    cp = sub.add_parser("collect")
    cp.add_argument("--url", required=True, help="X/Twitter profile URL")
    cp.add_argument("--token", required=True, help="X auth_token cookie value")
    cp.add_argument("--db", default="scweet_state.db", help="Scweet resume DB path")
    args = parser.parse_args()

    if args.cmd == "collect":
        results = collect(args.url, args.token, args.db)
        print(json.dumps(results, ensure_ascii=False, default=str))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
