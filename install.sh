#!/data/data/com.termux/files/usr/bin/bash
set -e

PROJECT="$HOME/foto-ai"
BIN="$HOME/bin"
CONFIG="$HOME/.config/foto-ai"

echo "================================"
echo "       FOTOAI INSTALLER"
echo "================================"

pkg update -y
pkg install -y python

python -m pip install requests watchdog pillow

mkdir -p "$PROJECT" "$BIN" "$CONFIG"
mkdir -p "$HOME/storage/shared/DCIM/Camera"
mkdir -p "$HOME/storage/shared/DCIM/Camera_Enhanced"

if [ ! -f "$PROJECT/ai_edit.py" ] || [ ! -f "$PROJECT/watch_camera.py" ]; then
  echo "File proyek tidak lengkap di $PROJECT"
  echo "Ekstrak semua file proyek ke ~/foto-ai terlebih dahulu."
  exit 1
fi

cat > "$BIN/fotoai" <<'COMMANDS'
#!/data/data/com.termux/files/usr/bin/bash

PROJECT="$HOME/foto-ai"
CONFIG="$HOME/.config/foto-ai"
PIDFILE="$CONFIG/watch.pid"

case "$1" in
  setup)
    read -rsp "Masukkan API key OpenAI: " KEY
    echo
    if [ -z "$KEY" ]; then
      echo "API key kosong."
      exit 1
    fi
    umask 077
    printf 'export OPENAI_API_KEY=%q\n' "$KEY" > "$CONFIG/key.sh"
    unset KEY
    echo "API key tersimpan secara lokal."
    ;;
  start)
    if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
      echo "FotoAI sudah berjalan."
      exit 0
    fi
    [ -f "$CONFIG/key.sh" ] && source "$CONFIG/key.sh"
    if [ -z "$OPENAI_API_KEY" ]; then
      echo "Atur API key dulu: fotoai setup"
      exit 1
    fi
    cd "$PROJECT"
    nohup python "$PROJECT/watch_camera.py" > "$CONFIG/watch.log" 2>&1 &
    echo $! > "$PIDFILE"
    sleep 2
    if kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
      echo "FotoAI dijalankan."
    else
      rm -f "$PIDFILE"
      echo "Pemantau gagal mulai. Periksa: fotoai log"
      exit 1
    fi
    ;;
  stop)
    if [ -f "$PIDFILE" ]; then
      kill "$(cat "$PIDFILE")" 2>/dev/null || true
      rm -f "$PIDFILE"
      echo "Perintah berhenti dikirim."
    else
      echo "PID pemantau tidak ditemukan."
    fi
    ;;
  status)
    if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
      echo "FotoAI terdeteksi berjalan."
    else
      echo "FotoAI tidak terdeteksi berjalan."
    fi
    ;;
  log)
    if [ -f "$CONFIG/watch.log" ]; then
      tail -n 40 "$CONFIG/watch.log"
    else
      echo "Log belum tersedia. Jalankan: fotoai start"
    fi
    ;;
  edit)
    if [ -z "$2" ]; then
      echo "Pakai: fotoai edit /lokasi/foto.jpg"
      exit 1
    fi
    [ -f "$CONFIG/key.sh" ] && source "$CONFIG/key.sh"
    python "$PROJECT/ai_edit.py" "$2"
    ;;
  *)
    echo "FotoAI Tools"
    echo "Perintah: setup | start | stop | status | log | edit"
    ;;
esac
COMMANDS

chmod +x "$BIN/fotoai"

if ! grep -qF 'export PATH="$HOME/bin:$PATH"' "$HOME/.bashrc" 2>/dev/null; then
  echo 'export PATH="$HOME/bin:$PATH"' >> "$HOME/.bashrc"
fi

echo
echo "Instalasi selesai."
echo "Buka ulang Termux atau jalankan: source ~/.bashrc"
echo "Lalu atur API key dengan: fotoai setup"
