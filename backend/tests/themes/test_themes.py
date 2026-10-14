"""The Python Cerrado 2026 themes, as the default profile installs them."""

from pythoncerrado.site.themes import THEMES
from sc.voltolighttheme.utils import themes

import pytest


class TestThemes:
    @pytest.fixture(autouse=True)
    def _setup(self, portal) -> None:
        self.portal = portal

    @pytest.mark.parametrize("theme_id", sorted(THEMES))
    def test_values(self, theme_id: str):
        """The registry holds exactly the values in ``THEMES``."""
        assert themes.theme_values(theme_id) == THEMES[theme_id]

    def test_theme_ids(self):
        """The add-on's default theme stays alongside the three 2026 themes."""
        assert themes.theme_ids() == sorted([*THEMES, themes.DEFAULT_THEME_ID])

    @pytest.mark.parametrize("theme_id", sorted(THEMES))
    def test_font(self, theme_id: str):
        """Every theme uses Outfit, which the frontend add-on loads."""
        values = themes.theme_values(theme_id)
        assert values["font_family_primary"] == "Outfit, sans-serif"
        assert values["font_family_secondary"] == "Outfit, sans-serif"
