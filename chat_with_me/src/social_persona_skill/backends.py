from __future__ import annotations
from pathlib import Path
from typing import List
import re

from .models import CorpusEntry
from .runtime import RuntimeManager
from .adapters import normalize


def _slug_from_url(url: str) -> str:
    url = url.rstrip("/")
    return re.sub(r"[^a-zA-Z0-9_\-]", "_", url.split("/")[-1])[:40]


def _platform_from_url(url: str) -> str:
    url_lower = url.lower()
    if "x.com" in url_lower or "twitter.com" in url_lower:
        return "x"
    if "xiaohongshu.com" in url_lower or "xhslink.com" in url_lower:
        return "xiaohongshu"
    if "instagram.com" in url_lower:
        return "instagram"
    if "zhihu.com" in url_lower:
        return "zhihu"
    if "github.com" in url_lower:
        return "github"
    raise ValueError(f"Cannot detect platform from URL: {url!r}")


class Backend:
    platform: str

    def collect(self, url: str) -> List[CorpusEntry]:
        raise NotImplementedError

    def bio(self, url: str) -> str:
        raise NotImplementedError

    def display_name(self, url: str) -> str:
        return _slug_from_url(url)


class XBackend(Backend):
    platform = "x"

    def __init__(self, runtime: RuntimeManager):
        self.runtime = runtime

    def collect(self, url: str) -> List[CorpusEntry]:
        import subprocess, json, sys
        helper = Path(__file__).parent / "backend_helpers" / "scweet_collect.py"
        py = self.runtime._venv_python("x")
        token = self.runtime.get_auth_token("x")
        db = str(self.runtime.scweet_db())
        result = subprocess.run(
            [py, str(helper), "collect", f"--url={url}", f"--token={token}", f"--db={db}"],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(f"Scweet collect failed:\n{result.stderr}")
        raw = json.loads(result.stdout)
        return normalize("x", raw)

    def display_name(self, url: str) -> str:
        parts = url.rstrip("/").split("/")
        return parts[-1].lstrip("@") if parts else _slug_from_url(url)


class XiaohongshuBackend(Backend):
    platform = "xiaohongshu"

    def __init__(self, runtime: RuntimeManager):
        self.runtime = runtime

    def collect(self, url: str) -> List[CorpusEntry]:
        import subprocess, json
        helper = Path(__file__).parent / "backend_helpers" / "xiaohongshu_collect.py"
        py = self.runtime._venv_python("xiaohongshu")
        repo = self.runtime.backend_repo("xiaohongshu")
        state_dir = self.runtime.browser_state_dir("xiaohongshu")
        result = subprocess.run(
            [py, str(helper), "collect",
             f"--url={url}",
             f"--state-dir={state_dir}",
             f"--repo={repo}"],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(f"MediaCrawler collect failed:\n{result.stderr}")
        raw = json.loads(result.stdout)
        return normalize("xiaohongshu", raw)

    def display_name(self, url: str) -> str:
        slug = _slug_from_url(url)
        return slug if slug else "xiaohongshu_user"


_BACKENDS = {
    "x": XBackend,
    "xiaohongshu": XiaohongshuBackend,
}


def get_backend(platform: str, runtime: RuntimeManager) -> Backend:
    cls = _BACKENDS.get(platform)
    if cls is None:
        raise ValueError(f"Platform {platform!r} is not yet supported.")
    return cls(runtime)


def detect_platform(url: str) -> str:
    return _platform_from_url(url)


def slug_from_url(url: str) -> str:
    return _slug_from_url(url)
