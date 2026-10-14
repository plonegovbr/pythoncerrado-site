from collections.abc import Generator
from plone.app.testing import applyProfile
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.base.interfaces import IPloneSiteRoot

import pytest


@pytest.fixture(scope="class")
def portal(portal_class) -> Generator[IPloneSiteRoot]:
    """Yield the class-scoped Plone site with the example content imported."""
    setRoles(portal_class, TEST_USER_ID, ["Manager"])
    applyProfile(portal_class, "pythoncerrado.site:initial")
    yield portal_class
