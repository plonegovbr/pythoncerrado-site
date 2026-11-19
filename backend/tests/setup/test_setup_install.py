from pythoncerrado.site import PACKAGE_NAME

import pytest


class TestSetupInstall:
    def test_addon_installed(self, installer):
        """Test if pythoncerrado.site is installed."""
        assert installer.is_product_installed(PACKAGE_NAME) is True

    def test_browserlayer(self, browser_layers):
        """Test that IBrowserLayer is registered."""
        from pythoncerrado.site.interfaces import IBrowserLayer

        assert IBrowserLayer in browser_layers

    def test_latest_version(self, profile_last_version):
        """Test latest version of default profile."""
        assert profile_last_version(f"{PACKAGE_NAME}:default") == "20261119001"

    def test_certificates_installed(self, installer):
        """collective.certificates comes with the default profile."""
        assert installer.is_product_installed("collective.certificates") is True

    @pytest.mark.parametrize(
        "token", ["outfit-regular", "outfit-semibold", "outfit-bold"]
    )
    def test_certificate_fonts(self, portal, token: str):
        """The install points collective.certificates at the Outfit fonts."""
        from collective.certificates.fonts.registry import all_fonts

        assert token in all_fonts()

    @pytest.mark.parametrize(
        "permission",
        [
            "collective.certificates: Add CertificateTemplate",
            "collective.certificates: Add Certificate",
        ],
    )
    @pytest.mark.parametrize(
        "role,allowed",
        [
            ("Manager", True),
            ("Site Administrator", True),
            ("Editor", False),
            ("Contributor", False),
        ],
    )
    def test_certificate_add_permissions(
        self, portal, permission: str, role: str, allowed: bool
    ):
        """Only managers and site administrators add templates and certificates."""
        roles = {
            item["name"]
            for item in portal.rolesOfPermission(permission)
            if item["selected"]
        }
        assert (role in roles) is allowed

    def test_themes_profile_installed(self, setup_tool):
        """The Themes control panel comes with sc.voltolighttheme:default."""
        version = setup_tool.getLastVersionForProfile("sc.voltolighttheme:default")
        # "unknown", never None, for a profile that was not installed.
        assert version != "unknown"
