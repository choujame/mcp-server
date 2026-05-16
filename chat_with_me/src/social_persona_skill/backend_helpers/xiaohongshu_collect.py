"""
Xiaohongshu collection helper — runs inside the MediaCrawler venv.
Usage:
  python xiaohongshu_collect.py login  --state-dir=<dir> --repo=<path>
  python xiaohongshu_collect.py collect --url=<url> --state-dir=<dir> --repo=<path>
Output: JSON array of note dicts to stdout.
"""
from __future__ import annotations
import argparse
import json
import sys
import os
import re
from pathlib import Path


def _user_id_from_url(url: str) -> str:
    match = re.search(r"user/profile/([a-zA-Z0-9]+)", url)
    if match:
        return match.group(1)
    return url.rstrip("/").split("/")[-1]


def do_login(state_dir: str, repo: str) -> None:
    sys.path.insert(0, repo)
    try:
        import asyncio
        from playwright.async_api import async_playwright

        async def _login():
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=False)
                context = await browser.new_context()
                page = await context.new_page()
                await page.goto("https://www.xiaohongshu.com")
                print("[xiaohongshu] Please scan the QR code to log in...")
                print("[xiaohongshu] Waiting 60 seconds for login...")
                await page.wait_for_timeout(60000)
                Path(state_dir).mkdir(parents=True, exist_ok=True)
                await context.storage_state(path=str(Path(state_dir) / "state.json"))
                await browser.close()
                print("[xiaohongshu] Login state saved.")

        asyncio.run(_login())
    except Exception as e:
        print(f"[xiaohongshu] Login error: {e}", file=sys.stderr)
        sys.exit(1)


def do_collect(url: str, state_dir: str, repo: str) -> list:
    sys.path.insert(0, repo)
    state_file = Path(state_dir) / "state.json"
    if not state_file.exists():
        print("[xiaohongshu] Not logged in. Run: backend login xiaohongshu", file=sys.stderr)
        return []

    user_id = _user_id_from_url(url)
    try:
        import asyncio
        from playwright.async_api import async_playwright
        import json as _json

        results = []

        async def _collect():
            async with async_playwright() as p:
                context = await p.chromium.launch_persistent_context(
                    user_data_dir=state_dir,
                    headless=True,
                )
                page = await context.new_page()

                collected = []

                async def _intercept(resp):
                    if "api/sns/web/v1/user_posted" in resp.url:
                        try:
                            data = await resp.json()
                            notes = data.get("data", {}).get("notes", [])
                            collected.extend(notes)
                        except Exception:
                            pass

                page.on("response", _intercept)
                await page.goto(f"https://www.xiaohongshu.com/user/profile/{user_id}")
                await page.wait_for_timeout(5000)

                # Scroll to load more
                for _ in range(5):
                    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    await page.wait_for_timeout(2000)

                await context.close()
                results.extend(collected)

        asyncio.run(_collect())
        return results
    except Exception as e:
        print(f"[xiaohongshu] Collect error: {e}", file=sys.stderr)
        return []


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", choices=["login", "collect"])
    parser.add_argument("--url", default="")
    parser.add_argument("--state-dir", required=True)
    parser.add_argument("--repo", required=True)
    args = parser.parse_args()

    if args.cmd == "login":
        do_login(args.state_dir, args.repo)
    elif args.cmd == "collect":
        results = do_collect(args.url, args.state_dir, args.repo)
        print(json.dumps(results, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
