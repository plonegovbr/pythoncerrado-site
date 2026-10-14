from pythoncerrado.site import PACKAGE_NAME


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
        assert profile_last_version(f"{PACKAGE_NAME}:default") == "20261013001"

    def test_themes_profile_installed(self, setup_tool):
        """The Themes control panel comes with sc.voltolighttheme:default."""
        version = setup_tool.getLastVersionForProfile("sc.voltolighttheme:default")
        # "unknown", never None, for a profile that was not installed.
        assert version != "unknown"
