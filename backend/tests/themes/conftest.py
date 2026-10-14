from collections.abc import Generator
from plone.base.interfaces import IPloneSiteRoot

import pytest


@pytest.fixture(scope="class")
def portal(portal_class) -> Generator[IPloneSiteRoot]:
    """Yield the class-scoped Plone site."""
    yield portal_class
