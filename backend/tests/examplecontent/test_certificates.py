"""The certificates folder, as the initial profile creates it."""

from plone import api
from pythoncerrado.site.certificates import FOLDER_TEXT
from pythoncerrado.site.certificates import TEMPLATES

import pytest


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


class TestCertificates:
    @pytest.fixture(autouse=True)
    def _setup(self, portal) -> None:
        self.portal = portal
        self.folder = api.content.get(path="/2026/certificados")

    def test_folder(self):
        """The folder is published, out of the navigation, with the message."""
        assert self.folder is not None
        assert self.folder.exclude_from_nav is True
        assert api.content.get_state(self.folder) == "published"
        texts = [
            block["plaintext"]
            for block in self.folder.blocks.values()
            if block["@type"] == "slate"
        ]
        assert texts == list(FOLDER_TEXT)

    def test_templates(self):
        """The folder holds the three templates, in this order."""
        assert self.folder.objectIds() == list(TEMPLATES)

    @pytest.mark.parametrize("template_id", list(TEMPLATES))
    def test_renders(self, template_id: str):
        """Each template renders its sample data as a PNG."""
        template = self.folder[template_id]

        data = {**template.sample_data, **template.computed_values("0" * 32)}
        image = template.render(data, "png")

        assert image.startswith(PNG_SIGNATURE)
