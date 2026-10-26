from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance
import sys

src = Path(sys.argv[1]).expanduser()
outdir = Path.home() / "storage/shared/DCIM/Camera_Enhanced"
outdir.mkdir(parents=True, exist_ok=True)

if not src.is_file():
    print("Foto tidak ditemukan:", src)
    raise SystemExit(1)

out = outdir / (src.stem + "_enhanced.jpg")

with Image.open(src) as original:
    img = ImageOps.exif_transpose(original).convert("RGB")
    img = ImageOps.autocontrast(img, cutoff=0.3)
    img = ImageEnhance.Color(img).enhance(1.05)
    img = ImageEnhance.Contrast(img).enhance(1.04)
    img = ImageEnhance.Sharpness(img).enhance(1.15)
    img.save(out, "JPEG", quality=95, optimize=True)

print("Berhasil:", out)
