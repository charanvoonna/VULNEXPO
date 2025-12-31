# modules/vuln_detect_engine.py

"""
Nmap engine for VULNEXPO / TraceNet.
Streams nmap output live and parses OPEN services reliably.
"""

import subprocess
import shlex
import signal
import platform
from typing import List, Dict, Any

from utils.colors import INFO, MODULE, ERROR, RESET


# --------------------------------------------------
# PARSER
# --------------------------------------------------
def _parse_nmap_services(output: str) -> List[Dict[str, Any]]:
    """
    Parse OPEN services from standard nmap -sV output.
    Expected format:
    PORT/PROTO  STATE  SERVICE  VERSION...
    """
    services: List[Dict[str, Any]] = []

    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue

        # Skip headers
        if line.startswith("PORT") or line.startswith("Nmap"):
            continue

        parts = line.split()
        if len(parts) < 3:
            continue

        port_proto = parts[0]
        state = parts[1]
        service = parts[2]

        if state.lower() != "open":
            continue

        try:
            port, proto = port_proto.split("/")
            port = int(port)
        except Exception:
            continue

        version = " ".join(parts[3:]) if len(parts) > 3 else ""

        services.append({
            "port": port,
            "proto": proto,
            "state": state,
            "service": service,
            "version": version,
            "version_parsed": version
        })

    return services


# --------------------------------------------------
# ENGINE
# --------------------------------------------------
def run_nmap(target: str, aggressive: bool = False, extra_args: str = "") -> Dict[str, Any]:
    is_windows = platform.system().lower().startswith("win")

    if aggressive:
        if is_windows:
            cmd = f"nmap -p- -sV --version-all -T4 --script=default,vuln {extra_args} {target}"
        else:
            cmd = f"nmap -p- -sV --version-all -O --osscan-guess -T4 --script=default,vuln {extra_args} {target}"
    else:
        cmd = f"nmap -sV {extra_args} {target}"

    print(INFO + f"[DEBUG] Running command: {cmd}" + RESET)

    raw_output: List[str] = []
    stderr_output: List[str] = []

    try:
        proc = subprocess.Popen(
            shlex.split(cmd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        # STREAM STDOUT LIVE
        for line in proc.stdout:
            print(line.rstrip())
            raw_output.append(line)

        # READ STDERR
        for line in proc.stderr:
            stderr_output.append(line)

        proc.wait()

    except KeyboardInterrupt:
        try:
            proc.send_signal(signal.SIGINT)
            proc.kill()
        except Exception:
            pass
        raise

    except FileNotFoundError:
        return {
            "target": target,
            "raw": "",
            "errors": "nmap not found",
            "services": []
        }

    except Exception as e:
        return {
            "target": target,
            "raw": "",
            "errors": str(e),
            "services": []
        }

    output_text = "".join(raw_output)
    services = _parse_nmap_services(output_text)

    print(INFO + f"[*] Service detection completed: {len(services)} services found" + RESET)
    for s in services:
        print(
            MODULE +
            f"    {s['port']}/{s['proto']}  {s['service']}  {s['version']}" +
            RESET
        )

    print(INFO + "[*] Scan finished." + RESET)

    return {
        "target": target,
        "raw": output_text,
        "errors": "".join(stderr_output),
        "services": services
    }
