# utils/banner.py
from datetime import datetime
from colorama import Fore, Style
from utils.colors import INFO, MODULE, RESET

BANNER_ASCII = r"""
██╗   ██╗██╗   ██╗██╗     ███╗   ██╗██╗  ██╗██╗  ███████╗██████╗  ██████╗ 
██║   ██║██║   ██║██║     ████╗  ██║██║ ██╔╝██║  ██╔════╝██╔══██╗██╔════╝ 
██║   ██║██║   ██║██║     ██╔██╗ ██║█████╔╝ ██║  █████╗  ██████╔╝██║  ███╗
██║   ██║╚██╗ ██╔╝██║     ██║╚██╗██║██╔═██╗ ██║  ██╔══╝  ██╔══██╗██║   ██║
╚██████╔╝ ╚████╔╝ ███████╗██║ ╚████║██║  ██╗██║  ███████╗██║  ██║╚██████╔╝
 ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚══════╝╚═╝  ╚═╝ ╚═════╝
"""

def _center_line(text, width=70):
    text = str(text)
    if len(text) >= width:
        return text
    pad = (width - len(text)) // 2
    return " " * pad + text

def print_banner(app="VULNEXPO", version="0.1"):
    # visual frame elements
    top_border = "/" + "-" * 70 + "\\"
    bot_border = "\\" + "-" * 70 + "/"
    sep = "|" + " " * 70 + "|"

    # print top frame
    print(Fore.BLUE + top_border + Style.RESET_ALL)
    print(Fore.BLUE + "|" + _center_line("") + " " * (70 - len(_center_line(""))) + "|" + Style.RESET_ALL)

    # ASCII art (blue)
    for line in BANNER_ASCII.splitlines():
        print(Fore.BLUE + "| " + _center_line(line, 66) + " |" + Style.RESET_ALL)

    # boxed subtitle and version (all blue)
    boxed = f"[ {app} v{version} ]"
    print(Fore.BLUE + "| " + _center_line("") + " |" + Style.RESET_ALL)
    print(Fore.BLUE + "| " + _center_line(boxed, 66) + " |" + Style.RESET_ALL)

    # small info/separator lines
    print(Fore.BLUE + "|" + " " * 70 + "|" + Style.RESET_ALL)
    print(Fore.BLUE + bot_border + Style.RESET_ALL)
    print()

    # status section under the framed banner (uses your color constants)
    print(INFO + f"[*] Started: {datetime.utcnow().isoformat()} UTC" + RESET)
    print(MODULE + f"[*] Modules loaded: vuln_detect , exploit" + RESET)
    print()
