"""Render the social preview card. Requires Pillow."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
image = Image.new("RGB", (1200, 630), "#605c52")
draw = ImageDraw.Draw(image)
font_dir = Path("C:/Windows/Fonts")
bold = font_dir / "arialbd.ttf"
regular = font_dir / "arial.ttf"

draw.line((80, 84, 1120, 84), fill="#938b76", width=2)
draw.text((80, 128), "Brian Mulder", font=ImageFont.truetype(str(bold), 36), fill="#f0d39b")
for y, line in zip((242, 319, 396), ("Software, AI", "and things", "worth building.")):
    draw.text((80, y), line, font=ImageFont.truetype(str(bold), 60), fill="#f7f1df")
draw.line((80, 535, 1120, 535), fill="#938b76", width=2)
draw.text((80, 557), "Software engineer · Consultant · Sydney", font=ImageFont.truetype(str(regular), 28), fill="#eae2cf")
image.save(ROOT / "social-card.png", optimize=True)
