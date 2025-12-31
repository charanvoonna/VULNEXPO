import os
import yaml

DEFAULTS = {
    "app": {"name": "VULNEXPO", "version": "0.1"},
    "io": {
        "results_dir": "results",
        "sessions_dir": "sessions",
        "reports_dir": "reports",
        "logs_dir": "logs"
    }
}

class Config:
    def __init__(self, cfg):
        self._cfg = cfg

    @classmethod
    def load(cls, path="config/config.yml"):
        if not os.path.exists(path):
            return cls(DEFAULTS)

        try:
            with open(path, "r") as f:
                loaded = yaml.safe_load(f) or {}
        except Exception:
            loaded = {}

        # Merge with defaults (simple shallow merge)
        merged = DEFAULTS.copy()
        for k, v in loaded.items():
            merged[k] = v

        return cls(merged)

    def get(self, *keys, default=None):
        node = self._cfg
        for k in keys:
            node = node.get(k)
            if node is None:
                return default
        return node
