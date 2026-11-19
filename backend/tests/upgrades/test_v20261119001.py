"""Upgrade to 20261119001: certificates of the 2026 edition."""

from . import PROFILE
from plone import api
from plone.base.utils import get_installer
from Products.GenericSetup.tool import SetupTool
from pythoncerrado.site.certificates import ADD_PERMISSIONS
from pythoncerrado.site.certificates import FOLDER_ID
from pythoncerrado.site.certificates import FONT_DIR_RECORD
from pythoncerrado.site.certificates import FONTS_DIR
from pythoncerrado.site.certificates import SIGNATURE_ID
from pythoncerrado.site.certificates import TEMPLATES
from pythoncerrado.site.upgrades.v20261119001 import ADDON

import pytest


SOURCE = "20261021001"
DESTINATION = "20261119001"


class TestUpgrade:
    """The steps from ``20261021001`` to ``20261119001``."""

    @pytest.fixture(autouse=True)
    def _setup(self, portal, setup_tool: SetupTool) -> None:
        """Put the site at the source version: no add-on, no folder."""
        self.portal = portal
        self.setup_tool = setup_tool
        with api.env.adopt_roles(["Manager"]):
            if "2026" not in portal.objectIds():
                api.content.create(
                    container=portal, type="Tech Event", id="2026", title="2026"
                )
            self.edition = portal["2026"]
            if FOLDER_ID in self.edition.objectIds():
                api.content.delete(obj=self.edition[FOLDER_ID])
            api.addon.uninstall(ADDON)
        for permission in ADD_PERMISSIONS:
            portal.manage_permission(permission, roles=[], acquire=False)
        setup_tool.setLastVersionForProfile(PROFILE, SOURCE)

    @pytest.fixture
    def font_dir_unset(self, setup_tool: SetupTool) -> None:
        """Clear the font directory after the add-on is back.

        The record only exists while the add-on is installed, so it is cleared
        by running the add-on's profile first.
        """
        api.addon.install(ADDON)
        api.portal.set_registry_record(FONT_DIR_RECORD, "")

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
        """The site at the source version is offered these two steps."""
        steps = self._steps()

        assert [(s["ssource"], s["sdest"]) for s in steps] == [
            (SOURCE, DESTINATION),
            (SOURCE, DESTINATION),
        ]

    def test_installs_the_addon(self):
        """The add-on's profile is installed and its version recorded."""
        installer = get_installer(self.portal)
        assert installer.is_product_installed(ADDON) is False

        self._upgrade()

        assert installer.is_product_installed(ADDON) is True
        version = self.setup_tool.getLastVersionForProfile(f"{ADDON}:default")
        assert version != "unknown"

    @pytest.mark.parametrize("permission", ADD_PERMISSIONS)
    @pytest.mark.parametrize("role", ["Manager", "Site Administrator"])
    def test_grants_add_permissions(self, permission: str, role: str):
        """Managers and site administrators may add templates and certificates."""
        self._upgrade()

        roles = {
            item["name"]
            for item in self.portal.rolesOfPermission(permission)
            if item["selected"]
        }
        assert role in roles

    def test_sets_the_font_dir(self, font_dir_unset):
        """The add-on reads the Outfit fonts from this package."""
        assert api.portal.get_registry_record(FONT_DIR_RECORD) == ""

        self._upgrade()

        assert api.portal.get_registry_record(FONT_DIR_RECORD) == str(FONTS_DIR)

    def test_creates_the_folder(self):
        """The folder is published and out of the navigation."""
        self._upgrade()

        folder = self.edition[FOLDER_ID]
        assert folder.exclude_from_nav is True
        assert api.content.get_state(folder) == "published"

    @pytest.mark.parametrize("template_id", list(TEMPLATES))
    def test_creates_the_template(self, template_id: str):
        """Each template has its signature and a blueprint that validates.

        Validation checks that the Outfit fonts and the signature exist.
        """
        self._upgrade()

        template = self.edition[FOLDER_ID][template_id]
        assert template.portal_type == "CertificateTemplate"
        assert template.title == TEMPLATES[template_id]["title"]
        assert template.page_size() == (2338, 1652)
        background = TEMPLATES[template_id]["background"]
        assert template.background.data == background.read_bytes()
        assert template[SIGNATURE_ID].portal_type == "Image"
        assert template.validate_blueprint() == []

    def test_keeps_an_edited_template(self):
        """A template already in the folder is not replaced."""
        self._upgrade()
        template = self.edition[FOLDER_ID]["palestrante-python-cerrado"]
        template.title = "Changed here"
        self.setup_tool.setLastVersionForProfile(PROFILE, SOURCE)

        self._upgrade()

        assert self.edition[FOLDER_ID]["palestrante-python-cerrado"].title == (
            "Changed here"
        )
