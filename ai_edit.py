from pathlib import Path
import os
import sys
import base64
import requests
import shutil
import subprocess

if len(sys.argv) != 2:
    print("Pakai: python ai_edit.py /lokasi/foto.jpg")
    raise SystemExit(1)

api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    print("API key belum aktif. Periksa konfigurasi Termux.")
    raise SystemExit(1)

src = Path(sys.argv[1]).expanduser()
if not src.is_file():
    print("Foto tidak ditemukan:", src)
    raise SystemExit(1)

prompt_file = Path.home() / "foto-ai" / "prompt.txt"
prompt = prompt_file.read_text(encoding="utf-8").strip()

storage = Path.home() / "storage/shared/DCIM"
outdir = storage / "Camera_Enhanced"
camera_dir = storage / "Camera"
outdir.mkdir(parents=True, exist_ok=True)
camera_dir.mkdir(parents=True, exist_ok=True)

out = outdir / f"{src.stem}_AI.png"
gallery_out = camera_dir / f"{src.stem}_AI.png"

url = "https://api.openai.com/v1/images/edits"
headers = {"Authorization": f"Bearer {api_key}"}
data = {
    "model": "gpt-image-2.5-sunburst",
    "prompt": prompt,
    "quality": "medium",
    "size": "auto",
    "output_format": "png",
}

print("Mengirim foto ke AI. Tunggu beberapa saat...")

try:
    with src.open("rb") as photo:
        response = requests.post(
            url,
            headers=headers,
            data=data,
            files={"image": (src.name, photo)},
            timeout=300,
        )

    if not response.ok:
        try:
            err = response.json().get("error", {}).get("message", response.text)
        except Exception:
            err = response.text
        print("API gagal:", response.status_code, str(err)[:1200])
        raise SystemExit(1)

    result = response.json()
    encoded = result["data"][0]["b64_json"]
    image_bytes = base64.b64decode(encoded)

    temp = out.with_suffix(".tmp")
    temp.write_bytes(image_bytes)
    temp.replace(out)
    print("Berhasil disimpan:", out)

    shutil.copy2(out, gallery_out)
    print("Salinan Galeri:", gallery_out)

    scan = subprocess.run(
        [
            "am", "broadcast",
            "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE",
            "-d", gallery_out.resolve().as_uri(),
        ],
        capture_output=True,
        text=True,
        timeout=15,
    )
    print("Permintaan pemindaian media dikirim.")

except requests.RequestException as exc:
    print("Koneksi API bermasalah:", exc)
    raise SystemExit(1)
except (KeyError, ValueError) as exc:
    print("Respons AI tidak sesuai format:", exc)
    raise SystemExit(1)
except (OSError, subprocess.SubprocessError) as exc:
    print("Foto AI tersimpan, tetapi proses salinan/pemindaian gagal:", exc)
