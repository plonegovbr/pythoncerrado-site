"""Upgrade to 20261119001: certificates of the 2026 edition."""

from plone import api
from Products.GenericSetup.tool import SetupTool
from pythoncerrado.site import logger
from pythoncerrado.site.certificates import create_certificates
from pythoncerrado.site.certificates import grant_add_permissions
from pythoncerrado.site.certificates import set_font_dir


#: The add-on this version installs.
ADDON = "collective.certificates"


def install_certificates(setup_tool: SetupTool) -> None:
    """Install collective.certificates, its fonts and its add permissions.

    :param setup_tool: The ``portal_setup`` tool.
    """
    api.addon.install(ADDON)
    logger.info("Installed %s", ADDON)
    grant_add_permissions(api.portal.get())
    set_font_dir()


def add_certificates_folder(setup_tool: SetupTool) -> None:
    """Create ``/2026/certificados`` and its three certificate templates.

    :param setup_tool: The ``portal_setup`` tool.
    """
    create_certificates(api.portal.get())
