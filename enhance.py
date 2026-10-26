from PIL import Image, ImageOps, ImageEnhance
from pathlib import Path
import time

SOURCE = Path.home() / "storage/shared/DCIM/Camera"
OUTPUT = Path.home() / "storage/shared/DCIM/Camera_Enhanced"

EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

def enhance(src):
    try:
        # Tunggu sampai penulisan file selesai
        old_size = -1
        stable = 0

        for _ in range(30):
            if not src.exists():
                return

            size = src.stat().st_size

            if size == old_size and size > 0:
                stable += 1
            else:
                stable = 0

            if stable >= 2:
                break

            old_size = size
            time.sleep(1)

        if not src.exists() or src.stat().st_size == 0:
            return

        output = OUTPUT / (src.stem + "_enhanced.jpg")

        if output.exists():
            return

        with Image.open(src) as original:
            img = ImageOps.exif_transpose(original)
            img = img.convert("RGB")

            # Koreksi ringan agar warna tidak berlebihan
            img = ImageOps.autocontrast(img, cutoff=0.3)
            img = ImageEnhance.Color(img).enhance(1.05)
            img = ImageEnhance.Contrast(img).enhance(1.04)
            img = ImageEnhance.Sharpness(img).enhance(1.15)

            img.save(
                output,
                "JPEG",
                quality=95,
                optimize=True
            )

        print(f"[OK] {src.name} -> {output.name}", flush=True)

    except Exception as e:
        print(f"[ERROR] {src.name}: {e}", flush=True)

def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)

    if not SOURCE.is_dir():
        print(f"Folder kamera tidak ditemukan: {SOURCE}")
        print("Periksa lokasi foto di HP kamu.")
        return

    seen = set()
    print("Pemantau foto aktif.", flush=True)
    print(f"Memantau: {SOURCE}", flush=True)
    print(f"Hasil: {OUTPUT}", flush=True)

    # Abaikan foto lama saat pertama dijalankan
    for p in SOURCE.iterdir():
        if p.is_file() and p.suffix.lower() in EXTENSIONS:
            seen.add(str(p))

    print("Sekarang ambil foto baru untuk menguji.", flush=True)

    while True:
        try:
            for p in SOURCE.iterdir():
                if not p.is_file():
                    continue

                if p.suffix.lower() not in EXTENSIONS:
                    continue

                key = str(p)

                if key not in seen:
                    seen.add(key)
                    enhance(p)

            time.sleep(2)

        except KeyboardInterrupt:
            print("\nPemantau dihentikan.")
            break

        except Exception as e:
            print(f"[ERROR] Pemantauan: {e}", flush=True)
            time.sleep(3)

if __name__ == "__main__":
    main()
