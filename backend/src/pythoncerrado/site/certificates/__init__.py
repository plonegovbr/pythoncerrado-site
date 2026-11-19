"""Certificates of the 2026 edition.

The ``/2026/certificados`` folder, out of the navigation, tells people that
their certificates were sent by email. It holds the three certificate
templates, which share one background image, the brand font (Outfit) and a
signature. The signature shipped here is a placeholder: production replaces
the ``assinatura`` Image item of each template with the real one.
"""

from copy import deepcopy
from pathlib import Path
from plone import api
from plone.base.interfaces import IPloneSiteRoot
from plone.namedfile.file import NamedBlobImage
from pythoncerrado.site import logger
from typing import Any


#: Permissions that collective.certificates grants to no role.
ADD_PERMISSIONS: tuple[str, ...] = (
    "collective.certificates: Add CertificateTemplate",
    "collective.certificates: Add Certificate",
)
#: Roles that may add templates and certificates.
ADD_ROLES: tuple[str, ...] = ("Manager", "Site Administrator")

#: Registry record naming the directory collective.certificates reads extra
#: fonts from. It takes an absolute path, so it is set when the site is
#: installed or upgraded, from where this package is.
FONT_DIR_RECORD = "collective.certificates.extra_font_dir"
FONTS_DIR = Path(__file__).parent / "fonts"
#: Font tokens, from the file names in :data:`FONTS_DIR`.
FONT_REGULAR = "outfit-regular"
FONT_SEMIBOLD = "outfit-semibold"
FONT_BOLD = "outfit-bold"

EDITION_PATH = "/2026"
FOLDER_ID = "certificados"
FOLDER_TITLE = "Certificados"
FOLDER_DESCRIPTION = "Certificados da Python Cerrado 2026 e do Cerrado Sprint."
FOLDER_TEXT = (
    "Os certificados da Python Cerrado 2026 e do Cerrado Sprint são "
    "enviados por email para as pessoas participantes e palestrantes. "
    "Procure na sua caixa de entrada, e também na pasta de spam, a "
    "mensagem com o certificado em anexo ou com o link para baixá-lo.",
    "Cada certificado traz um QR code e um endereço de verificação, que "
    "confirmam a sua autenticidade.",
)

IMAGES_DIR = Path(__file__).parent / "images"
BACKGROUND = IMAGES_DIR / "background.png"
#: Background of the Cerrado Sprint, with the Plone, PloneGov-BR and Cerrado
#: Sprint logos.
BACKGROUND_SPRINT = IMAGES_DIR / "background-sprint.png"
#: Color of the plain areas of each background, behind the QR code.
PLAIN_COLOR = "#fcf8f0"
PLAIN_COLOR_SPRINT = "#f7fafc"
#: Placeholder signature, drawn by ``scripts/fake_signature.py``.
SIGNATURE = IMAGES_DIR / "signature.png"
#: Id of the Image item holding the signature in each template.
SIGNATURE_ID = "assinatura"

#: Positions follow the plain areas of the background: text in
#: (120, 420)-(1700, 1300), signature in (120, 1330)-(600, 1450),
#: responsible person in (120, 1460)-(760, 1520), QR code in
#: (1878, 1150)-(2218, 1490), certificate code below it.
PAGE = {"width": 2338, "height": 1652}
TEXT_COLOR = "#3b2a1e"
ACCENT_COLOR = "#0f6b55"
TEXT_X = 120
TEXT_WIDTH = 1580
DATE_FORMAT = "day-month-year"


def _text(
    element_id: str, y: int, content: str, size: int, **extra: Any
) -> dict[str, Any]:
    """Return a left-aligned text element of the certificate body.

    :param element_id: Element id, unique in the blueprint.
    :param y: Baseline position, in page pixels.
    :param content: Text, with ``{{ field }}`` tokens.
    :param size: Font size, in page pixels.
    :param extra: Other element keys, overriding the defaults.
    :returns: A text element.
    """
    element = {
        "id": element_id,
        "type": "text",
        "x": TEXT_X,
        "y": y,
        "anchor": "start",
        "baseline": "alphabetic",
        "font": FONT_REGULAR,
        "size": size,
        "color": TEXT_COLOR,
        "content": content,
        "max_width": TEXT_WIDTH,
        "fit": "shrink",
    }
    element.update(extra)
    return element


#: Baselines of the lines that say what the person did.
BODY_LINES = (960, 1045, 1131)
#: Where the venue line says the edition happened.
VENUE = "nas dependências do CEUB Asa Norte, Brasília, DF"
#: Width of "apresentou a palestra" in Outfit Regular at 44 px, plus the gap
#: before the talk title. Measure again if the font or size changes.
TALK_X = TEXT_X + 436 + 12


def blueprint(
    title: str,
    body: list[dict[str, Any]],
    role: str = "Organização da Python Cerrado",
    plain_color: str = PLAIN_COLOR,
) -> dict[str, Any]:
    """Return a blueprint: the shared heading and footer around a body.

    :param title: Certificate title, such as ``Certificado de Palestrante``.
    :param body: Text elements saying what the person did.
    :param role: Line below the responsible person.
    :param plain_color: Color of the background's plain areas, behind the QR
        code.
    :returns: The blueprint, as ``collective.certificates`` validates it.
    """
    elements = [
        _text("title", 560, title, 96, font=FONT_BOLD, color=ACCENT_COLOR),
        _text("certify", 700, "Certificamos que", 44),
        _text("name", 850, "{{ full_name }}", 110, font=FONT_SEMIBOLD),
        *body,
        {
            "id": "signature",
            "type": "image",
            "x": 120,
            "y": 1330,
            "width": 480,
            "height": 120,
            "asset": SIGNATURE_ID,
        },
        _text(
            "signer",
            1500,
            "{{ responsible_person }}",
            34,
            font=FONT_SEMIBOLD,
            max_width=640,
        ),
        _text("role", 1550, role, 26, max_width=640),
        {
            "id": "qr",
            "type": "qrcode",
            "x": 1898,
            "y": 1170,
            "size": 300,
            "content": "{{ verification_url }}",
            "ec": "M",
            "fg": TEXT_COLOR,
            "bg": plain_color,
        },
        {
            "id": "uid",
            "type": "text",
            "x": 2048,
            "y": 1550,
            "anchor": "middle",
            "baseline": "alphabetic",
            "font": FONT_REGULAR,
            "size": 16,
            "color": TEXT_COLOR,
            "content": "{{ certificate_uid }}",
            "max_width": 340,
            "fit": "shrink",
        },
    ]
    return {"version": 1, "page": dict(PAGE), "elements": elements}


SPEAKER_BODY = [
    _text("participation", BODY_LINES[0], "apresentou a palestra", 44),
    _text(
        "palestra",
        BODY_LINES[0],
        "{{ event_name }}",
        44,
        x=TALK_X,
        font=FONT_SEMIBOLD,
        max_width=TEXT_X + TEXT_WIDTH - TALK_X,
    ),
    _text(
        "period",
        BODY_LINES[1],
        "durante a Python Cerrado 2026, ocorrida nos dias "
        "{{ event_start_date|date }} e {{ event_end_date|date }},",
        44,
    ),
    _text("local", BODY_LINES[2], f"{VENUE}.", 44),
]

ATTENDEE_BODY = [
    _text(
        "participation",
        BODY_LINES[0],
        "participou da {{ event_name }}, ocorrida nos dias "
        "{{ event_start_date|date }} e {{ event_end_date|date }},",
        44,
    ),
    _text("local", BODY_LINES[1], f"{VENUE},", 44),
    _text(
        "period",
        BODY_LINES[2],
        "com carga horária de {{ total_hours }} horas.",
        44,
    ),
]

SPRINT_BODY = [
    _text("participation", BODY_LINES[0], "participou do {{ event_name }},", 44),
    _text(
        "period",
        BODY_LINES[1],
        "de {{ event_start_date|date }} a {{ event_end_date|date }}, "
        "com carga horária de {{ total_hours }} horas.",
        44,
    ),
]


def _sample(event_name: str, start: str, end: str, hours: str) -> dict[str, str]:
    """Return sample values for the designer and the preview.

    :param event_name: Event name.
    :param start: Start date, ISO format.
    :param end: End date, ISO format.
    :param hours: Total hours.
    :returns: Sample data.
    """
    return {
        "full_name": "Maria da Silva",
        "event_name": event_name,
        "event_start_date": start,
        "event_end_date": end,
        "responsible_person": "Pessoa Responsável",
        "total_hours": hours,
    }


#: The templates inside the folder, by id.
TEMPLATES: dict[str, dict[str, Any]] = {
    "palestrante-python-cerrado": {
        "title": "Palestrante da Python Cerrado",
        "background": BACKGROUND,
        "blueprint": blueprint("Certificado de Palestrante", SPEAKER_BODY),
        # The talk title goes in ``event_name``: collective.certificates has
        # no field of its own for it yet.
        "sample_data": _sample(
            "Tópico relevante sobre Python", "2026-11-06", "2026-11-07", "16"
        ),
    },
    "participante-python-cerrado": {
        "title": "Participante da Python Cerrado",
        "background": BACKGROUND,
        "blueprint": blueprint("Certificado de Participação", ATTENDEE_BODY),
        "sample_data": _sample("Python Cerrado 2026", "2026-11-06", "2026-11-07", "12"),
    },
    "participante-cerrado-sprint": {
        "title": "Participante do Cerrado Sprint",
        "background": BACKGROUND_SPRINT,
        "blueprint": blueprint(
            "Certificado de Participação",
            SPRINT_BODY,
            role="Comunidade PloneGov-BR",
            plain_color=PLAIN_COLOR_SPRINT,
        ),
        "sample_data": _sample("Cerrado Sprint 2026", "2026-11-03", "2026-11-06", "28"),
    },
}


def _blocks() -> tuple[dict[str, dict], list[str]]:
    """Return the folder's blocks: its title and the message.

    :returns: Blocks by id, and their order.
    """
    blocks: dict[str, dict] = {"certificados-title": {"@type": "title"}}
    for index, paragraph in enumerate(FOLDER_TEXT):
        blocks[f"certificados-text-{index}"] = {
            "@type": "slate",
            "plaintext": paragraph,
            "value": [{"type": "p", "children": [{"text": paragraph}]}],
        }
    return blocks, list(blocks)


def grant_add_permissions(portal: IPloneSiteRoot) -> None:
    """Let managers and site administrators add templates and certificates.

    :param portal: The Plone site.
    """
    for permission in ADD_PERMISSIONS:
        portal.manage_permission(permission, roles=list(ADD_ROLES), acquire=False)
        logger.info("Granted %s to %s", permission, ", ".join(ADD_ROLES))


def set_font_dir() -> None:
    """Point collective.certificates at the Outfit fonts of this package."""
    api.portal.set_registry_record(FONT_DIR_RECORD, str(FONTS_DIR))
    logger.info("Set %s to %s", FONT_DIR_RECORD, FONTS_DIR)


def _image(path: Path) -> NamedBlobImage:
    """Return a new image value with the contents of a file.

    :param path: The image file.
    :returns: The image value.
    """
    return NamedBlobImage(data=path.read_bytes(), filename=path.name)


def create_folder(edition: Any) -> Any:
    """Create the certificates folder, or return the existing one.

    :param edition: The 2026 ``Tech Event``.
    :returns: The folder.
    """
    folder = edition.get(FOLDER_ID)
    if folder is not None:
        logger.info("Folder %s already exists", folder.absolute_url_path())
        return folder
    blocks, order = _blocks()
    folder = api.content.create(
        container=edition,
        type="Document",
        id=FOLDER_ID,
        title=FOLDER_TITLE,
        description=FOLDER_DESCRIPTION,
        exclude_from_nav=True,
        blocks=blocks,
        blocks_layout={"items": order},
    )
    api.content.transition(obj=folder, transition="publish")
    logger.info("Created %s", folder.absolute_url_path())
    return folder


def create_templates(folder: Any) -> list[Any]:
    """Create the certificate templates missing from the folder.

    Templates that already exist are left alone: they may have been edited
    in the designer, or have the real signature.

    :param folder: The certificates folder.
    :returns: The templates created.
    """
    created = []
    for template_id, data in TEMPLATES.items():
        if template_id in folder.objectIds():
            logger.info("Template %s already exists", template_id)
            continue
        template = api.content.create(
            container=folder,
            type="CertificateTemplate",
            id=template_id,
            title=data["title"],
            background=_image(data["background"]),
            blueprint=deepcopy(data["blueprint"]),
            sample_data=dict(data["sample_data"]),
            date_format=DATE_FORMAT,
        )
        api.content.create(
            container=template,
            type="Image",
            id=SIGNATURE_ID,
            title="Assinatura",
            image=_image(SIGNATURE),
        )
        logger.info("Created template %s", template.absolute_url_path())
        created.append(template)
    return created


def create_certificates(portal: IPloneSiteRoot) -> Any:
    """Create the certificates folder and its templates in the 2026 edition.

    :param portal: The Plone site.
    :returns: The folder, or ``None`` when the site has no 2026 edition.
    """
    edition = api.content.get(path=EDITION_PATH)
    if edition is None:
        logger.warning("No %s edition: certificates not created", EDITION_PATH)
        return None
    with api.env.adopt_roles(["Manager"]):
        folder = create_folder(edition)
        create_templates(folder)
    return folder
