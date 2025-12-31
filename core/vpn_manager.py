# core/vpn_manager.py
"""
Day-1 VPN Manager Stub
This file only prevents errors. No real VPN or proxy logic yet.
"""

class VPNManager:
    def __init__(self):
        pass

    def start_openvpn(self, ovpn_path: str):
        # Fake behavior for now
        return {
            "ok": False,
            "msg": "OpenVPN not implemented yet (Day-1 stub)"
        }

    def set_proxy_env(self, proxy_url: str):
        # Fake behavior for now
        return {
            "ok": True,
            "msg": f"Proxy set (simulated): {proxy_url}"
        }
