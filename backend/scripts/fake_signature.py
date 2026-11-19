"""Draw the placeholder signature of the certificate templates.

The image only fills the signature area until the real one replaces it, on
the production site, in each template's ``assinatura`` Image item.

Run from ``backend/``::

    .venv/bin/python scripts/fake_signature.py
"""

from collective.certificates.fonts.registry import BUNDLED
from pathlib import Path
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


#: Where the templates read the signature from.
TARGET = (
    Path(__file__).parent.parent
    / "src"
    / "pythoncerrado"
    / "site"
    / "certificates"
    / "images"
    / "signature.png"
)
#: Twice the 480 x 120 signature area of the certificate.
SIZE = (960, 240)
INK = (59, 42, 30, 255)
TEXT = "Assinatura"


def draw() -> Image.Image:
    """Return the placeholder signature: handwritten text and a flourish.

    :returns: An RGBA image with a transparent background.
    """
    image = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    canvas = ImageDraw.Draw(image)
    font = ImageFont.truetype(str(BUNDLED["caveat"].path), 150)
    canvas.text((60, 20), TEXT, font=font, fill=INK)
    flourish = [(40, 200), (260, 186), (520, 196), (760, 178), (920, 160)]
    canvas.line(flourish, fill=INK, width=6, joint="curve")
    return image


def main() -> None:
    """Write the placeholder signature over :data:`TARGET`."""
    draw().save(TARGET, optimize=True)
    print(f"Wrote {TARGET}")


if __name__ == "__main__":
    main()
