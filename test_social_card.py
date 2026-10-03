"""Exercise portable generation without changing published assets."""
from pathlib import Path
import hashlib
import subprocess
import sys
import tempfile
from PIL import Image

ROOT = Path(__file__).resolve().parent
published = ROOT / 'social-card.png'
before = published.read_bytes()
with tempfile.TemporaryDirectory() as folder:
    outputs = [Path(folder) / f'card-{i}.png' for i in range(2)]
    for output in outputs:
        subprocess.run([sys.executable, str(ROOT / 'build_social_card.py'),
                        '--output', str(output)], cwd=folder, check=True)
        with Image.open(output) as image:
            assert image.size == (1200, 630)
            assert image.mode == 'RGB'
            assert image.getpixel((1199, 629)) == (96, 92, 82)
    assert outputs[0].read_bytes() == outputs[1].read_bytes()
assert published.read_bytes() == before
for name, expected in {
    'Regular': 'bade59d822652f76e6941aa87b40a87c13d1cc70db98ededb5011127efafd1d3',
    'Bold': '1b5f2da6f4cadce4c05b9ecebe3a6fcd374eb95ae443605e799f4c3287978939',
}.items():
    font = ROOT / 'assets' / 'fonts' / f'LiberationSans-{name}.ttf'
    assert hashlib.sha256(font.read_bytes()).hexdigest() == expected
print('PASS: generation outside repo, repeatable image, dimensions/colors, font provenance, published asset unchanged')
