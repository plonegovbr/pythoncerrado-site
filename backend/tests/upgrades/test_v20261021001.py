"""Upgrade to 20261021001: themes of the 2018 and 2019 editions."""

from . import PROFILE
from Products.GenericSetup.tool import SetupTool
from pythoncerrado.site.themes import THEMES
from pythoncerrado.site.upgrades.v20261021001 import THEME_IDS
from sc.voltolighttheme.utils import themes

import pytest


SOURCE = "20261013001"
DESTINATION = "20261021001"


class TestUpgrade:
    """The step from ``20261013001`` to ``20261021001``."""

    @pytest.fixture(autouse=True)
    def _setup(self, setup_tool: SetupTool) -> None:
        """Put the site back at the source version, without the new themes."""
        self.setup_tool = setup_tool
        setup_tool.setLastVersionForProfile(PROFILE, SOURCE)
        for theme_id in THEME_IDS:
            themes.delete_theme(theme_id)

    def _steps(self) -> list[dict]:
        """Return the upgrade steps available from the source version.

        ``listUpgrades`` gives the steps of an ``upgradeSteps`` group as one
        list, and a lone ``upgradeStep`` as a bare info.
        """
        steps: list[dict] = []
        for entry in self.setup_tool.listUpgrades(PROFILE):
            steps.extend(entry if isinstance(entry, list) else [entry])
        return steps

    def _upgrade(self) -> None:
        for step in self._steps():
            step["step"].doStep(self.setup_tool)

    def test_available(self):
        """The site at the source version is offered exactly this step."""
        steps = self._steps()

        assert [(s["ssource"], s["sdest"]) for s in steps] == [(SOURCE, DESTINATION)]

    @pytest.mark.parametrize("theme_id", THEME_IDS)
    def test_creates_the_theme(self, theme_id: str):
        """Running it installs the theme with the values of ``THEMES``."""
        assert not themes.theme_exists(theme_id)

        self._upgrade()

        assert themes.theme_values(theme_id) == THEMES[theme_id]

    def test_updates_an_existing_theme(self):
        """A theme created by hand before the upgrade gets the shipped values."""
        themes.create_theme("pythoncerrado-2018", {"name": "Criado à mão"})

        self._upgrade()

        assert themes.theme_values("pythoncerrado-2018") == THEMES["pythoncerrado-2018"]

    def test_leaves_other_themes_alone(self):
        """It writes the two new themes rather than re-importing the registry."""
        themes.update_theme("pythoncerrado-2026", {"name": "Changed here"})

        self._upgrade()

        assert themes.theme_values("pythoncerrado-2026")["name"] == "Changed here"
