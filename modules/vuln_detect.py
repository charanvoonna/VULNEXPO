# modules/vuln_detect.py

from typing import Dict, Any
from packaging import version

from modules.vuln_detect_engine import run_nmap
from modules.vuln_signatures import SIGNATURES
from utils.colors import INFO, SUCCESS, ERROR, RESET


class VulnDetectModule:
    """
    Vulnerability Detection Module
    - LIVE        : Normal Nmap scan
    - AGGRESSIVE  : Aggressive Nmap scan
    """

    def __init__(self, io_mgr=None, msf=None):
        self.io = io_mgr
        self.msf = msf
        self.opts = {}

    # --------------------------------------------------
    # OPTIONS
    # --------------------------------------------------
    def set_options(self, options: dict):
        self.opts = options

    # --------------------------------------------------
    # MAIN RUN
    # --------------------------------------------------
    def run(self) -> Dict[str, Any]:

        # ---- read options ----
        target = self.opts.get("TARGET")
        live = str(self.opts.get("LIVE", "false")).lower() in ("1", "true", "yes")
        aggressive = str(self.opts.get("AGGRESSIVE", "false")).lower() in ("1", "true", "yes")

        # ---- validation ----
        if not target:
            print(ERROR + "[!] TARGET not set." + RESET)
            return {"status": "error", "error": "TARGET not set"}

        if aggressive and not live:
            print(ERROR + "[!] LIVE mode is required for AGGRESSIVE scan." + RESET)
            print(INFO + "    Use: set LIVE true" + RESET)
            return {"status": "aborted"}

        if not live:
            print(ERROR + "[!] LIVE mode is required to run vulnerability scan." + RESET)
            return {"status": "aborted"}

        # ---- confirmation for aggressive ----
        if aggressive:
            confirm = input("LIVE + AGGRESSIVE enabled. Type 'yes' to continue: ")
            if confirm.lower() != "yes":
                print(ERROR + "[!] Aborted by user." + RESET)
                return {"status": "aborted"}

        # ---- start scan ----
        print(INFO + f"[*] Starting vulnerability scan on {target}" + RESET)
        print(INFO + ("[*] Scan mode: AGGRESSIVE" if aggressive else "[*] Scan mode: NORMAL") + RESET)

        # ---- run nmap ----
        scan = run_nmap(target=target, aggressive=aggressive)

        # ---- handle errors ----
        errors = scan.get("errors")
        if errors:
            print(ERROR + "[!] Nmap warnings/errors:" + RESET)
            print(errors.strip())

        services = scan.get("services", [])

        # --------------------------------------------------
        # PRINT OPEN SERVICES  (RESTORED OLD BEHAVIOR)
        # --------------------------------------------------
        if services:
            print(SUCCESS + "[+] Open services discovered:" + RESET)

            for svc in services:
                port = svc.get("port")
                proto = svc.get("protocol", "tcp")
                name = svc.get("service", "unknown")
                product = svc.get("product") or ""
                version_str = svc.get("version") or ""

                details = " ".join(p for p in [product, version_str] if p).strip()

                line = f"    {port}/{proto:<4} {name:<15}"
                if details:
                    line += f" {details}"

                print(SUCCESS + line + RESET)

        print(SUCCESS + f"[+] Services detected: {len(services)}" + RESET)

        # --------------------------------------------------
        # CVE Candidate Mapping (UNCHANGED)
        # --------------------------------------------------
        cve_candidates = []

        for svc in services:
            svc_name = (svc.get("service") or "").lower()
            svc_version_raw = svc.get("version_parsed") or ""
            svc_port = svc.get("port")

            try:
                svc_version = version.parse(svc_version_raw) if svc_version_raw else None
            except Exception:
                svc_version = None

            for sig in SIGNATURES:
                sig_service = (sig.get("service") or "").lower()
                aliases = [sig_service] + [a.lower() for a in sig.get("service_aliases", [])]

                if svc_name not in aliases:
                    continue

                rule = sig.get("version_match", {})
                rule_type = rule.get("type", "any")

                version_ok = False

                try:
                    if rule_type == "any":
                        version_ok = True

                    elif rule_type == "exact" and svc_version:
                        version_ok = svc_version == version.parse(rule.get("value"))

                    elif rule_type == "range" and svc_version:
                        min_v = version.parse(rule.get("min"))
                        max_v = version.parse(rule.get("max"))
                        version_ok = min_v <= svc_version < max_v

                except Exception:
                    version_ok = False

                if not version_ok:
                    continue

                cve_candidates.append({
                    "service": svc_name,
                    "port": svc_port,
                    "detected_version": svc.get("version"),
                    "cve": sig.get("cve"),
                    "description": sig.get("description"),
                    "exploit_module": sig.get("exploit_module"),
                    "confidence": sig.get("base_confidence", 0.0),
                    "type": sig.get("type")
                })

        # --------------------------------------------------
        # Display CVE candidates
        # --------------------------------------------------
        if cve_candidates:
            print(SUCCESS + f"\n[+] CVE Candidates Found: {len(cve_candidates)}" + RESET)
            for c in cve_candidates:
                print(
                    ERROR +
                    f"[!] {c['service']} ({c['detected_version']}) on port {c['port']}\n"
                    f"    CVE: {c['cve']}\n"
                    f"    Exploit: {c['exploit_module']}\n"
                    f"    Confidence: {c['confidence']}\n"
                    + RESET
                )
        else:
            print(INFO + "[*] No known CVE candidates found." + RESET)

        # --------------------------------------------------
        # Save results
        # --------------------------------------------------
        result = {
            "target": target,
            "aggressive": aggressive,
            "services": services,
            "cve_candidates": cve_candidates
        }

        if self.io:
            path = self.io.save_json(f"{target}.vulns.json", result)
            print(INFO + f"[*] Results saved to {path}" + RESET)
            return {"status": "saved", "path": path}

        return {"status": "success", "result": result}
