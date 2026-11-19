from Products.GenericSetup.tool import SetupTool
from pythoncerrado.site.certificates import set_font_dir


def post_install(setup_tool: SetupTool) -> None:
    """Finish the install with what a profile file cannot hold.

    The font directory of collective.certificates is an absolute path, known
    only once the package is installed.

    :param setup_tool: The ``portal_setup`` tool.
    """
    set_font_dir()
