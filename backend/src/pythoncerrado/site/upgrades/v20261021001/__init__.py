"""Upgrade to 20261021001: themes of the 2018 and 2019 editions."""

from Products.GenericSetup.tool import SetupTool
from pythoncerrado.site import logger
from pythoncerrado.site.themes import THEMES
from sc.voltolighttheme.utils import themes


#: Themes added in this version, selected by the imported 2018 and 2019
#: ``Tech Event``\s.
THEME_IDS = ("pythoncerrado-2018", "pythoncerrado-2019")


def add_edition_themes(setup_tool: SetupTool) -> None:
    """Install the 2018 and 2019 theme records.

    Writes only these two themes, rather than re-importing the registry, which
    would reset every value changed on the site since it was installed.

    :param setup_tool: The ``portal_setup`` tool.
    """
    for theme_id in THEME_IDS:
        if themes.theme_exists(theme_id):
            themes.update_theme(theme_id, THEMES[theme_id])
            logger.info("Updated theme %s", theme_id)
        else:
            themes.create_theme(theme_id, THEMES[theme_id])
            logger.info("Created theme %s", theme_id)
