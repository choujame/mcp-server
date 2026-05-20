from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import subprocess
import sys

from .models import Platform


@dataclass
class RuntimeLayout:
    root: Path

    def __post_init__(self) -> None:
        self.root = Path(self.root)

    def ensure_base_dirs(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        (self.root / "backends").mkdir(exist_ok=True)
        (self.root / "state").mkdir(exist_ok=True)

    # ── paths ────────────────────────────────────────────────────────────

    @property
    def auth_tokens_file(self) -> Path:
        return self.root / "auth_tokens"

    def backend_venv(self, platform: Platform) -> Path:
        return self.root / "backends" / platform.value / "venv"

    def backend_python(self, platform: Platform) -> Path:
        return self.backend_venv(platform) / "bin" / "python"

    def backend_repo(self, platform: Platform) -> Path:
        return self.root / "backends" / platform.value / "repo"

    def state_dir(self, platform: Platform) -> Path:
        d = self.root / "state" / platform.value
        d.mkdir(parents=True, exist_ok=True)
        return d

    def browser_state_dir(self, platform: Platform) -> Path:
        d = self.state_dir(platform) / "browser_state"
        d.mkdir(parents=True, exist_ok=True)
        return d

    def scweet_db(self) -> Path:
        return self.root / "backends" / "x" / "scweet_state.db"

    # ── auth tokens ──────────────────────────────────────────────────────

    def get_auth_token(self, platform: Platform) -> str:
        if not self.auth_tokens_file.exists():
            raise FileNotFoundError(
                f"Auth tokens file not found: {self.auth_tokens_file}\n"
                f"Create it and add your token. Format:\n"
                f"# X (twitter):\nyour_auth_token_here # token"
            )
        content = self.auth_tokens_file.read_text(encoding="utf-8")
        platform_key = {
            Platform.X: "X (twitter)",
            Platform.XIAOHONGSHU: "xiaohongshu",
        }.get(platform, platform.value)
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

    def write_auth_token_template(self, platform: Platform) -> None:
        existing = ""
        if self.auth_tokens_file.exists():
            existing = self.auth_tokens_file.read_text(encoding="utf-8")
        templates = {
            Platform.X: "\n# X (twitter):\nyour_auth_token_here # token\n",
            Platform.XIAOHONGSHU: "\n# xiaohongshu:\n# (uses browser scan — no token needed)\n",
        }
        tmpl = templates.get(platform, f"\n# {platform.value}:\nyour_token_here\n")
        section_header = tmpl.strip().split("\n")[0].strip("#").strip()
        if section_header not in existing:
            with self.auth_tokens_file.open("a", encoding="utf-8") as f:
                f.write(tmpl)
        print(f"[runtime] Auth token template written to: {self.auth_tokens_file}")

    # ── venv helpers ─────────────────────────────────────────────────────

    def _venv_pip(self, platform: Platform) -> str:
        venv_dir = self.backend_venv(platform)
        pip = venv_dir / "bin" / "pip"
        if not pip.exists():
            pip = venv_dir / "Scripts" / "pip.exe"
        return str(pip)

    def _create_venv(self, platform: Platform) -> Path:
        venv_dir = self.backend_venv(platform)
        if not self.backend_python(platform).exists():
            print(f"[runtime] Creating venv for {platform.value} backend...")
            subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
        return venv_dir

    # ── bootstrap ────────────────────────────────────────────────────────

    def _bootstrap_x(self) -> None:
        self._create_venv(Platform.X)
        pip = self._venv_pip(Platform.X)
        print("[runtime] Installing Scweet into x backend venv...")
        subprocess.run(
            [pip, "install", "git+https://github.com/Altimis/Scweet.git@master"],
            check=True,
        )
        print("[runtime] X backend ready.")

    def _bootstrap_xiaohongshu(self) -> None:
        repo_dir = self.backend_repo(Platform.XIAOHONGSHU)
        repo_dir.parent.mkdir(parents=True, exist_ok=True)
        if not (repo_dir / ".git").exists():
            print("[runtime] Cloning MediaCrawler...")
            subprocess.run(
                ["git", "clone", "--depth=1",
                 "https://github.com/NanmiCoder/MediaCrawler.git",
                 str(repo_dir)],
                check=True,
            )
        self._create_venv(Platform.XIAOHONGSHU)
        pip = self._venv_pip(Platform.XIAOHONGSHU)
        req = repo_dir / "requirements.txt"
        if req.exists():
            print("[runtime] Installing MediaCrawler requirements...")
            subprocess.run([pip, "install", "-r", str(req)], check=True)
        print("[runtime] Xiaohongshu backend ready.")

    def bootstrap(self, platform: Platform) -> None:
        self.ensure_base_dirs()
        if platform == Platform.X:
            self._bootstrap_x()
        elif platform == Platform.XIAOHONGSHU:
            self._bootstrap_xiaohongshu()
        else:
            raise ValueError(f"Bootstrap not supported for platform: {platform!r}")

    # ── login ────────────────────────────────────────────────────────────

    def _login_x(self) -> None:
        needs_setup = (
            not self.auth_tokens_file.exists()
            or "your_auth_token_here" in self.auth_tokens_file.read_text()
        )
        if needs_setup:
            self.write_auth_token_template(Platform.X)
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
                token = self.get_auth_token(Platform.X)
                print(f"[login] X auth_token found ({token[:6]}...)")
            except Exception as e:
                print(f"[login] {e}")

    def _login_xiaohongshu(self) -> None:
        py = str(self.backend_python(Platform.XIAOHONGSHU))
        repo = self.backend_repo(Platform.XIAOHONGSHU)
        state_dir = self.browser_state_dir(Platform.XIAOHONGSHU)
        helper = Path(__file__).parent / "backend_helpers" / "xiaohongshu_collect.py"
        print("[login] Launching Xiaohongshu browser login (scan QR code)...")
        subprocess.run(
            [py, str(helper), "login", f"--state-dir={state_dir}", f"--repo={repo}"],
            check=True,
        )
        print("[login] Xiaohongshu login cached.")

    def login(self, platform: Platform) -> None:
        if platform == Platform.X:
            self._login_x()
        elif platform == Platform.XIAOHONGSHU:
            self._login_xiaohongshu()
        else:
            raise ValueError(f"Login not supported for platform: {platform!r}")
