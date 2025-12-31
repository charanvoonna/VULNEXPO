#!/usr/bin/env python3
# main.py — VULNEXPO Interactive Shell (Phase-1 STABLE)

import os
import platform

from utils.banner import print_banner
from utils.colors import PROMPT, INFO, SUCCESS, MODULE, ERROR, RESET
from utils.help_text import HELP_TEXT

from core.config import Config
from core.io_manager import IOManager
from core.vpn_manager import VPNManager

# Optional Metasploit adapter
try:
    from core.msf_adapter import MSFAdapter
except Exception:
    MSFAdapter = None

from modules.vuln_detect import VulnDetectModule
from modules.exploit import ExploitModule


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------
def clear_screen():
    os.system("cls" if platform.system().lower().startswith("win") else "clear")


def parse_bool(value):
    val = str(value).lower()
    if val in ("1", "true", "yes", "y", "on"):
        return True
    if val in ("0", "false", "no", "n", "off"):
        return False
    raise ValueError("Invalid boolean value")


# ------------------------------------------------------------------
# Shell State
# ------------------------------------------------------------------
class ShellState:
    def __init__(self):
        self.module_name = None
        self.options = {}
        self.modules = {}

    def set_option(self, key, value):
        self.options[key.upper()] = value

    def get_option(self, key, default=None):
        return self.options.get(key.upper(), default)


def prompt(state):
    if state.module_name:
        return f"VULNEXPO/{state.module_name.upper()}> "
    return "VULNEXPO> "


# ------------------------------------------------------------------
# Network prompt
# ------------------------------------------------------------------
def network_prompt(vpn_mgr):
    print(INFO + "VULNEXPO NETWORK OPTIONS :" + RESET)
    print("1) countine with  No VPN / Proxy (default)")
    print("2) use OpenVPN")
    print("3) use System Proxy")
    print("4) use Tor (9050)")
    choice = input("Choose [1-4]: ").strip() or "1"

    if choice == "1":
        print(INFO + "[*] Continuing without VPN." + RESET)
    elif choice == "2":
        path = input("Path to .ovpn: ").strip()
        if path:
            print(vpn_mgr.start_openvpn(path).get("msg"))
    elif choice == "3":
        proxy = input("Proxy URL: ").strip()
        if proxy:
            print(vpn_mgr.set_proxy_env(proxy).get("msg"))
    elif choice == "4":
        print(vpn_mgr.set_proxy_env("socks5://127.0.0.1:9050").get("msg"))
    else:
        print(ERROR + "Invalid option. Continuing without VPN." + RESET)


# ------------------------------------------------------------------
# Module loader
# ------------------------------------------------------------------
def load_modules(io_mgr, msf):
    return {
        "vuln_detect": VulnDetectModule(io_mgr, msf),
        "exploit": ExploitModule(io_mgr, msf),
    }


# ------------------------------------------------------------------
# CLI Loop
# ------------------------------------------------------------------
def prompt_loop(state):
    while True:
        try:
            line = input(PROMPT + prompt(state) + RESET).strip()
        except (KeyboardInterrupt, EOFError):
            print(ERROR + "\n[!] Exiting VulnExpo" + RESET)
            break

        if not line:
            continue

        parts = line.split()
        cmd = parts[0].lower()
        args = parts[1:]

        # ---------------- Core ----------------
        if cmd in ("exit", "quit"):
            break

        if cmd == "help":
            print(HELP_TEXT)
            continue

        if cmd == "clear":
            clear_screen()
            continue

        if cmd == "back":
            state.module_name = None
            print(INFO + "[*] Back to main context" + RESET)
            continue

        # ---------------- Use module ----------------
        if cmd == "use":
            if not args:
                print(ERROR + "Usage: use <vuln_detect|exploit>" + RESET)
                continue

            name = args[0].lower()
            if name in ("vd", "vuln", "vuln_detect"):
                state.module_name = "vuln_detect"
                print(MODULE + "[*] Loaded vuln_detect" + RESET)
            elif name in ("expl", "exploit"):
                state.module_name = "exploit"
                print(MODULE + "[*] Loaded exploit" + RESET)
            else:
                print(ERROR + "Unknown module" + RESET)
            continue

        # ---------------- Set options ----------------
        if cmd == "set":
            if len(args) < 2:
                print(ERROR + "Usage: set KEY VALUE" + RESET)
                continue

            key = args[0].upper()
            value = " ".join(args[1:])

            try:
                if key in ("LIVE", "VERBOSE", "AGGRESSIVE"):
                    value = parse_bool(value)
                if key in ("LPORT",):
                    value = int(value)

                state.set_option(key, value)
                print(SUCCESS + f"{key} => {value}" + RESET)
            except Exception as e:
                print(ERROR + str(e) + RESET)
            continue

        # ---------------- Exploit sub-commands ----------------
        if state.module_name == "exploit":
            exp = state.modules["exploit"]

            if cmd == "show":
                if not args:
                    print(ERROR + "[!] Usage: show <candidates|selected|options>" + RESET)
                    continue

                sub = args[0].lower()

                if sub == "candidates":
                    exp.show_candidates()
                    continue

                if sub == "selected":
                    exp.show_selected()
                    continue

                if sub == "options":
                    print(INFO + "Current options:" + RESET)
                    for k, v in state.options.items():
                        print(" ", k, v)
                    continue

                print(ERROR + "Unknown show option" + RESET)
                continue

            if cmd == "select":
                if not args or not args[0].isdigit():
                    print(ERROR + "[!] Usage: select <id>" + RESET)
                    continue

                exp.select(int(args[0]))
                continue

        # ---------------- Run ----------------
        if cmd == "run":
            if not state.module_name:
                print(ERROR + "No module loaded" + RESET)
                continue

            mod = state.modules[state.module_name]

            # vuln_detect accepts options, exploit handles internally
            if state.module_name != "exploit":
                if hasattr(mod, "set_options"):
                    mod.set_options(state.options)

            try:
                res = mod.run()
            except KeyboardInterrupt:
                print(ERROR + "\n[!] Interrupted" + RESET)
                continue
            except Exception as e:
                print(ERROR + str(e) + RESET)
                continue

            if isinstance(res, dict):
                print(SUCCESS + "[*] Module finished" + RESET)
            continue

        print(ERROR + f"Unknown command: {cmd}" + RESET)


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------
def main():
    cfg = Config.load()
    print_banner(cfg.get("app", "name"), cfg.get("app", "version"))

    vpn_mgr = VPNManager()
    network_prompt(vpn_mgr)

    io_mgr = IOManager(cfg)
    msf = MSFAdapter(cfg) if MSFAdapter else None

    state = ShellState()
    state.modules = load_modules(io_mgr, msf)

    prompt_loop(state)


if __name__ == "__main__":
    main()
