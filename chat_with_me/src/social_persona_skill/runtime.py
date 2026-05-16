from __future__ import annotations
from pathlib import Path
import os
import subprocess
import sys


class RuntimeManager:
    def __init__(self, runtime_root: Path):
        self.root = Path(runtime_root)
        self.root.mkdir(parents=True, exist_ok=True)

    # ── paths ────────────────────────────────────────────────────────────

    @property
    def auth_tokens_file(self) -> Path:
        return self.root / "auth_tokens"

    def backend_venv(self, platform: str) -> Path:
        return self.root / "backends" / platform / "venv"

    def backend_repo(self, platform: str) -> Path:
        return self.root / "backends" / platform / "repo"

    def browser_state_dir(self, platform: str) -> Path:
        d = self.root / "state" / platform / "browser_state"
        d.mkdir(parents=True, exist_ok=True)
        return d

    def scweet_db(self) -> Path:
        return self.root / "backends" / "x" / "scweet_state.db"

    # ── auth tokens ──────────────────────────────────────────────────────

    def get_auth_token(self, platform: str) -> str:
        if not self.auth_tokens_file.exists():
            raise FileNotFoundError(
                f"Auth tokens file not found: {self.auth_tokens_file}\n"
                f"Create it and add your token. Format:\n"
                f"# X (twitter):\nyour_auth_token_here # token"
            )
        content = self.auth_tokens_file.read_text(encoding="utf-8")
        platform_key = {"x": "X (twitter)", "xiaohongshu": "xiaohongshu"}.get(platform, platform)
        in_section = False
        for line in content.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                if platform_key.lower() in stripped.lower():
                    in_section = True
                continue
            if in_section:
                token = stripped.split("#")[0].strip()
                if token:
                    return token
        raise ValueError(
            f"No token found for platform {platform!r} in {self.auth_tokens_file}\n"
            f"Expected format:\n# X (twitter):\nyour_token_here # token"
        )

    def write_auth_token_template(self, platform: str) -> None:
        existing = ""
        if self.auth_tokens_file.exists():
            existing = self.auth_tokens_file.read_text(encoding="utf-8")
        templates = {
            "x": "\n# X (twitter):\nyour_auth_token_here # token\n",
            "xiaohongshu": "\n# xiaohongshu:\n# (uses browser scan — no token needed)\n",
        }
        tmpl = templates.get(platform, f"\n# {platform}:\nyour_token_here\n")
        if tmpl.strip().split("\n")[0].strip("#").strip() not in existing:
            with self.auth_tokens_file.open("a", encoding="utf-8") as f:
                f.write(tmpl)
        print(f"[runtime] Auth token template written to: {self.auth_tokens_file}")

    # ── venv helpers ─────────────────────────────────────────────────────

    def _create_venv(self, platform: str) -> Path:
        venv_dir = self.backend_venv(platform)
        if not (venv_dir / "bin" / "python").exists():
            print(f"[runtime] Creating venv for {platform} backend...")
            subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
        return venv_dir

    def _venv_python(self, platform: str) -> str:
        venv_dir = self.backend_venv(platform)
        py = venv_dir / "bin" / "python"
        if not py.exists():
            py = venv_dir / "Scripts" / "python.exe"
        return str(py)

    def _venv_pip(self, platform: str) -> str:
        venv_dir = self.backend_venv(platform)
        pip = venv_dir / "bin" / "pip"
        if not pip.exists():
            pip = venv_dir / "Scripts" / "pip.exe"
        return str(pip)

    # ── bootstrap ────────────────────────────────────────────────────────

    def bootstrap_x(self) -> None:
        venv = self._create_venv("x")
        pip = self._venv_pip("x")
        print("[runtime] Installing Scweet into x backend venv...")
        subprocess.run(
            [pip, "install", "git+https://github.com/Altimis/Scweet.git@master"],
            check=True,
        )
        print("[runtime] X backend ready.")

    def bootstrap_xiaohongshu(self) -> None:
        repo_dir = self.backend_repo("xiaohongshu")
        repo_dir.parent.mkdir(parents=True, exist_ok=True)
        if not (repo_dir / ".git").exists():
            print("[runtime] Cloning MediaCrawler...")
            subprocess.run(
                ["git", "clone", "--depth=1",
                 "https://github.com/NanmiCoder/MediaCrawler.git",
                 str(repo_dir)],
                check=True,
            )
        venv = self._create_venv("xiaohongshu")
        pip = self._venv_pip("xiaohongshu")
        req = repo_dir / "requirements.txt"
        if req.exists():
            print("[runtime] Installing MediaCrawler requirements...")
            subprocess.run([pip, "install", "-r", str(req)], check=True)
        print("[runtime] Xiaohongshu backend ready.")

    def bootstrap(self, platform: str) -> None:
        if platform == "x":
            self.bootstrap_x()
        elif platform == "xiaohongshu":
            self.bootstrap_xiaohongshu()
        else:
            raise ValueError(f"Unknown platform: {platform!r}")

    # ── login ────────────────────────────────────────────────────────────

    def login_x(self) -> None:
        if not self.auth_tokens_file.exists() or "your_auth_token_here" in self.auth_tokens_file.read_text():
            self.write_auth_token_template("x")
            print(
                "\n[login] Please add your X auth_token to:\n"
                f"  {self.auth_tokens_file}\n\n"
                "How to get it:\n"
                "  1. Log in to x.com\n"
                "  2. Open DevTools (F12) → Application → Cookies → https://x.com\n"
                "  3. Copy the value of 'auth_token'\n"
                "  4. Replace 'your_auth_token_here' in the file above\n"
            )
        else:
            try:
                token = self.get_auth_token("x")
                print(f"[login] X auth_token found ({token[:6]}...)")
            except Exception as e:
                print(f"[login] {e}")

    def login_xiaohongshu(self) -> None:
        py = self._venv_python("xiaohongshu")
        repo = self.backend_repo("xiaohongshu")
        state_dir = self.browser_state_dir("xiaohongshu")
        helper = Path(__file__).parent / "backend_helpers" / "xiaohongshu_collect.py"
        print("[login] Launching Xiaohongshu browser login (scan QR code)...")
        subprocess.run(
            [py, str(helper), "login", f"--state-dir={state_dir}", f"--repo={repo}"],
            check=True,
        )
        print("[login] Xiaohongshu login cached.")

    def login(self, platform: str) -> None:
        if platform == "x":
            self.login_x()
        elif platform == "xiaohongshu":
            self.login_xiaohongshu()
        else:
            raise ValueError(f"Unknown platform: {platform!r}")
