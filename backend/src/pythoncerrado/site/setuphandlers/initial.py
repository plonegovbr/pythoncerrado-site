from pathlib import Path
from plone import api
from plone.exportimport import importers
from Products.GenericSetup.tool import SetupTool
from pythoncerrado.site import logger

import json


EXAMPLE_CONTENT_FOLDER = Path(__file__).parent / "examplecontent"


def restore_rooms(content_folder: Path) -> int:
    """Set the rooms of schedule slots that the import could not set.

    The exporter writes items in path order, so ``<event>/grade/...`` slots are
    imported before the rooms under ``<event>/sobre/local``. The rooms vocabulary
    searches the catalog, rejects the not-yet-existing room, and the slot is
    created without it.

    :param content_folder: Folder holding the exported ``content`` items.
    :returns: Number of slots updated.
    """
    updated = 0
    for data_file in content_folder.glob("content/*/data.json"):
        data = json.loads(data_file.read_text())
        rooms = data.get("room")
        if not rooms:
            continue
        obj = api.content.get(UID=data["UID"])
        if obj is None or getattr(obj, "room", None):
            continue
        obj.room = set(rooms)
        obj.reindexObject()
        updated += 1
    return updated


def create_example_content(portal_setup: SetupTool):
    """Import content available at the examplecontent folder."""
    portal = api.portal.get()
    importer = importers.get_importer(portal)
    for line in importer.import_site(EXAMPLE_CONTENT_FOLDER):
        logger.info(line)
    updated = restore_rooms(EXAMPLE_CONTENT_FOLDER)
    if updated:
        logger.info(f"Restored the room of {updated} schedule slot(s)")
