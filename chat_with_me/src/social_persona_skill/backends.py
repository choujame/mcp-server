from __future__ import annotations
from pathlib import Path
from typing import Protocol, runtime_checkable
import json
import re
import subprocess

from .models import Platform, AccountInput, AccountRecord, CollectedAccount
from .runtime import RuntimeLayout
from .adapters import normalize


class BackendError(RuntimeError):
    pass


def platform_for_url(url: str) -> Platform:
    url_lower = url.lower()
    if "x.com" in url_lower or "twitter.com" in url_lower:
        return Platform.X
    if "xiaohongshu.com" in url_lower or "xhslink.com" in url_lower:
        return Platform.XIAOHONGSHU
    if "instagram.com" in url_lower:
        return Platform.INSTAGRAM
    if "zhihu.com" in url_lower:
        return Platform.ZHIHU
    if "github.com" in url_lower:
        return Platform.GITHUB
    raise ValueError(f"Cannot detect platform from URL: {url!r}")


@runtime_checkable
class Backend(Protocol):
    timeout_seconds: float

    @property
    def platform(self) -> Platform: ...

    def collect(self, account: AccountInput) -> CollectedAccount: ...


class ScweetBackend:
    """Collects X/Twitter posts using Scweet."""

    timeout_seconds: float = 120.0
    platform = Platform.X

    def __init__(self, layout: RuntimeLayout) -> None:
        self.layout = layout

    def collect(self, account: AccountInput) -> CollectedAccount:
        helper = Path(__file__).parent / "backend_helpers" / "scweet_collect.py"
        py = str(self.layout.backend_python(Platform.X))
        try:
            token = self.layout.get_auth_token(Platform.X)
        except (FileNotFoundError, ValueError) as exc:
            raise BackendError(
                f"X auth token not configured. Run: backend login x\n{exc}"
            ) from exc
        db = str(self.layout.scweet_db())

        result = subprocess.run(
            [py, str(helper), "collect",
             f"--url={account.url}",
             f"--token={token}",
             f"--db={db}"],
            capture_output=True,
            text=True,
            timeout=self.timeout_seconds,
        )
        if result.returncode != 0:
            raise BackendError(f"Scweet collect failed:\n{result.stderr}")

        try:
            raw = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise BackendError(f"Scweet output is not valid JSON: {exc}") from exc

        profile_id = _profile_id_from_x_url(account.url)
        display_name = profile_id
        account_rec = AccountRecord(
            platform=Platform.X,
            url=account.url,
            profile_id=profile_id,
            display_name=display_name,
        )
        corpus = normalize(Platform.X, account_rec, raw)
        return CollectedAccount(account=account_rec, corpus=corpus)


class XiaohongshuBackend:
    """Collects Xiaohongshu notes using MediaCrawler."""

    timeout_seconds: float = 180.0
    platform = Platform.XIAOHONGSHU

    def __init__(self, layout: RuntimeLayout) -> None:
        self.layout = layout

    def collect(self, account: AccountInput) -> CollectedAccount:
        helper = Path(__file__).parent / "backend_helpers" / "xiaohongshu_collect.py"
        py = str(self.layout.backend_python(Platform.XIAOHONGSHU))
        repo = self.layout.backend_repo(Platform.XIAOHONGSHU)
        state_dir = self.layout.browser_state_dir(Platform.XIAOHONGSHU)

        result = subprocess.run(
            [py, str(helper), "collect",
             f"--url={account.url}",
             f"--state-dir={state_dir}",
             f"--repo={repo}"],
            capture_output=True,
            text=True,
            timeout=self.timeout_seconds,
        )
        if result.returncode != 0:
            raise BackendError(f"MediaCrawler collect failed:\n{result.stderr}")

        try:
            raw = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise BackendError(f"MediaCrawler output is not valid JSON: {exc}") from exc

        profile_id = _profile_id_from_xhs_url(account.url)
        display_name = profile_id
        account_rec = AccountRecord(
            platform=Platform.XIAOHONGSHU,
            url=account.url,
            profile_id=profile_id,
            display_name=display_name,
        )
        corpus = normalize(Platform.XIAOHONGSHU, account_rec, raw)
        return CollectedAccount(account=account_rec, corpus=corpus)


def _profile_id_from_x_url(url: str) -> str:
    url = url.rstrip("/")
    match = re.search(r"(?:twitter|x)\.com/@?([^/?#]+)", url)
    if match:
        return match.group(1)
    return url.split("/")[-1].lstrip("@")


def _profile_id_from_xhs_url(url: str) -> str:
    match = re.search(r"user/profile/([a-zA-Z0-9]+)", url)
    if match:
        return match.group(1)
    return url.rstrip("/").split("/")[-1]


def build_backend_registry(layout: RuntimeLayout) -> dict[Platform, Backend]:
    return {
        Platform.X: ScweetBackend(layout),
        Platform.XIAOHONGSHU: XiaohongshuBackend(layout),
    }
