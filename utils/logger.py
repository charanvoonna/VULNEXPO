import time
from utils.colors import INFO, SUCCESS, ERROR, WARNING, RESET


class Logger:
    def __init__(self, enabled=True):
        self.enabled = enabled
        self.logs = []

    def _emit(self, prefix, color, message):
        timestamp = time.strftime("%H:%M:%S")
        plain = f"[{timestamp}] {prefix} {message}"
        colored = f"{color}{plain}{RESET}"

        # store plain text only (for result files)
        self.logs.append(plain)

        if self.enabled:
            print(colored)

    def info(self, message):
        self._emit("[*]", INFO, message)

    def success(self, message):
        self._emit("[+]", SUCCESS, message)

    def warning(self, message):
        self._emit("[!]", WARNING, message)

    def error(self, message):
        self._emit("[x]", ERROR, message)

    def dump(self):
        return self.logs
