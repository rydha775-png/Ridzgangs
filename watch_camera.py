from pathlib import Path
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler
import subprocess
import time

camera = Path.home() / "storage/shared/DCIM/Camera"
enhanced = Path.home() / "storage/shared/DCIM/Camera_Enhanced"
script = Path.home() / "foto-ai/ai_edit.py"

EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
processing = set()

def process(path):
    path = Path(path)
    if path.suffix.lower() not in EXTENSIONS or not path.is_file():
        return
    if path.stem.endswith("_AI") or path.name == "Foto_AI_Tes.png":
        return
    if path in processing:
        return

    processing.add(path)
    try:
        previous = -1
        stable = 0

        for _ in range(60):
            if not path.exists():
                return
            size = path.stat().st_size
            if size == previous and size > 0:
                stable += 1
                if stable >= 3:
                    break
            else:
                stable = 0
            previous = size
            time.sleep(1)
        else:
            print("File belum stabil, foto asli dipertahankan:", path.name, flush=True)
            return

        print("\nFoto baru:", path.name, flush=True)
        print("AI sedang memproses. Foto asli belum dihapus.", flush=True)

        result = subprocess.run(
            ["python", str(script), str(path)],
            check=False
        )

        if result.returncode != 0:
            print("AI gagal. Foto asli dipertahankan:", path.name, flush=True)
            return

        ai_file = enhanced / f"{path.stem}_AI.png"
        gallery_file = camera / f"{path.stem}_AI.png"

        if not ai_file.is_file() or ai_file.stat().st_size == 0:
            print("Hasil AI tidak ditemukan. Foto asli dipertahankan.", flush=True)
            return

        if not gallery_file.is_file() or gallery_file.stat().st_size == 0:
            print("Salinan Galeri tidak ditemukan. Foto asli dipertahankan.", flush=True)
            return

        print("Hasil AI tersimpan di kedua lokasi.", flush=True)

        try:
            path.unlink()
            print("Foto asli dihapus:", path.name, flush=True)
        except OSError as exc:
            print("Hasil AI aman, tetapi foto asli gagal dihapus:", exc, flush=True)

    except OSError as exc:
        print("Kesalahan file; foto asli dipertahankan jika masih ada:", exc, flush=True)
    finally:
        processing.discard(path)

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            process(event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            process(event.dest_path)

if not camera.is_dir():
    raise SystemExit(f"Folder kamera tidak ditemukan: {camera}")

enhanced.mkdir(parents=True, exist_ok=True)

print("Pemantau kamera aktif:", camera, flush=True)
print("Mode: hapus foto asli setelah hasil AI berhasil tersimpan.", flush=True)
print("Tekan Ctrl+C untuk berhenti.", flush=True)

observer = PollingObserver(timeout=2)
observer.schedule(Handler(), str(camera), recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
