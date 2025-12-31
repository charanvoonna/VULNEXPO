import os
import json
from datetime import datetime
from core.config import Config

class IOManager:
    """
    Minimal IO helper for TraceNet.
    Responsibilities:
    - ensure output directories exist
    - save JSON results atomically
    - save session JSON
    - save PoC markdown reports
    - write simple logs
    """

    def __init__(self, cfg: Config = None):
        self.cfg = cfg or Config.load()
        self.base = os.getcwd()
        # resolve directories from config (fall back to defaults)
        self.results_dir = self._resolve('io', 'results_dir', 'results')
        self.sessions_dir = self._resolve('io', 'sessions_dir', 'sessions')
        self.reports_dir = self._resolve('io', 'reports_dir', 'reports')
        self.logs_dir = self._resolve('io', 'logs_dir', 'logs')
        self._ensure_dirs()

    def _resolve(self, *keys_and_fallback):
        """
        Resolve nested config keys to a path.

        Usage:
            _resolve('io', 'results_dir', 'results')
        where the last positional argument is always the fallback directory name.

        This helper:
         - extracts fallback as the last positional arg
         - uses the preceding args as keys to lookup in the config
         - returns an absolute path (joined to project base) unless the value is absolute
        """
        if not keys_and_fallback:
            raise ValueError("No keys/fallback provided to _resolve")

        # last positional argument is treated as fallback
        *keys, fallback = keys_and_fallback

        # if no keys provided, just return joined fallback
        if not keys:
            return os.path.join(self.base, fallback)

        # try to get config value
        val = self.cfg.get(*keys, default=None)
        if not val:
            return os.path.join(self.base, fallback)
        return val if os.path.isabs(val) else os.path.join(self.base, val)

    def _ensure_dirs(self):
        for d in (self.results_dir, self.sessions_dir, self.reports_dir, self.logs_dir):
            try:
                os.makedirs(d, exist_ok=True)
            except Exception:
                # best-effort, we'll surface errors when saving
                pass

    def _atomic_write(self, path: str, text: str, mode: str = 'w') -> str:
        tmp = path + '.tmp'
        with open(tmp, mode, encoding='utf-8') as f:
            f.write(text)
        os.replace(tmp, path)
        return path

    def save_json(self, filename: str, data: dict) -> str:
        """Save JSON into results_dir. filename may be 'target.vulns.json' or just 'target'."""
        if not filename.endswith('.json'):
            filename = filename + '.json'
        full = os.path.join(self.results_dir, filename)
        text = json.dumps(data, indent=2, default=str)
        return self._atomic_write(full, text, mode='w')

    def save_session(self, target: str, session_data: dict) -> str:
        """Save exploit session metadata into sessions_dir as <target>.session.json"""
        fname = f"{target}.session.json"
        full = os.path.join(self.sessions_dir, fname)
        text = json.dumps(session_data, indent=2, default=str)
        return self._atomic_write(full, text, mode='w')

    def save_report_md(self, target: str, md_text: str) -> str:
        """Save PoC markdown into reports_dir as poC-<target>.md"""
        fname = f"poC-{target}.md"
        full = os.path.join(self.reports_dir, fname)
        return self._atomic_write(full, md_text, mode='w')

    def log(self, name: str, text: str) -> str:
        """Write a simple timestamped log file to logs_dir."""
        ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
        fname = f"{ts}-{name}.log"
        full = os.path.join(self.logs_dir, fname)
        return self._atomic_write(full, text, mode='w')
