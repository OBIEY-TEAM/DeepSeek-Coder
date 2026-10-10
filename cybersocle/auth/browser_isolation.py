"""
Browser Isolation & VPN Access Controller for CYBERSOCLE User Cells.
"""

from typing import Any


class CellBrowserIsolationController:
    """
    Manages user browser access rules based on cell health status and ship context.
    """

    @staticmethod
    def configure_cell_browser(ship_name: str, is_affected: bool) -> dict[str, Any]:
        if ship_name.upper() == "OFFICIEL" and not is_affected:
            return {
                "browser_enabled": True,
                "vpn_tunnel_active": True,
                "allowed_destinations": ["corporate-intranet.local", "internal-apps.company.com"],
                "policy": "SECURE_CORPORATE_VPN"
            }
        else:
            return {
                "browser_enabled": True,
                "vpn_tunnel_active": False,
                "allowed_destinations": [],
                "policy": "AIRGAPPED_HONEYPOT_NO_VPN"
            }
