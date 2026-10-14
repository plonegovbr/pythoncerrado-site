"""The example content, as the initial profile imports it."""

from plone import api
from zoneinfo import ZoneInfo

import pytest


BRASILIA = ZoneInfo("America/Sao_Paulo")


class TestExampleContent:
    @pytest.fixture(autouse=True)
    def _setup(self, portal) -> None:
        self.portal = portal

    def test_lightning_talks_room(self):
        """The slot keeps its room, although it is imported before the room."""
        talks = api.content.get(path="/2026/grade/20261107/palestras-relampago")
        room = api.content.get(path="/2026/sobre/local/auditorio-1")
        assert talks.room == {room.UID()}

    @pytest.mark.parametrize(
        "path,start,end",
        [
            ("/2026/grade/20261106/credenciamento", "08:00", "09:00"),
            ("/2026/grade/20261106/almoco", "12:00", "14:00"),
            ("/2026/grade/20261107/credenciamento", "08:00", "09:00"),
            ("/2026/grade/20261107/almoco", "12:00", "14:00"),
            ("/2026/grade/20261107/foto-dos-participantes", "15:50", "16:00"),
            ("/2026/grade/20261107/coffee-break", "16:00", "16:20"),
            ("/2026/grade/20261107/palestras-relampago", "17:00", "17:30"),
        ],
    )
    def test_slot_times(self, path: str, start: str, end: str):
        """Slots happen at these Brasília times, whatever the site timezone."""
        slot = api.content.get(path=path)
        assert slot.start.astimezone(BRASILIA).strftime("%H:%M") == start
        assert slot.end.astimezone(BRASILIA).strftime("%H:%M") == end

    @pytest.mark.parametrize(
        "path,theme",
        [
            ("/", "pythoncerrado-2026-terra-vermelha"),
            ("/2026", "pythoncerrado-2026"),
        ],
    )
    def test_theme(self, path: str, theme: str):
        assert api.content.get(path=path).theme == theme

    @pytest.mark.parametrize(
        "path,exists",
        [
            ("/2026/patrocine/apoio/ceub", True),
            ("/2026/patrocine/ouro/simples-consultoria", True),
            ("/2026/patrocine/apoio/uniprocessus", False),
            ("/2026/patrocine/ouro/ieee", False),
            ("/2026/patrocine/apoio/boss", False),
        ],
    )
    def test_sponsors(self, path: str, exists: bool):
        assert (api.content.get(path=path) is not None) is exists
