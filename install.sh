
#!/data/data/com.termux/files/usr/bin/bash
set -e

REPO="https://github.com/rydha775-png/Ridzgangs.git"
PROJECT="$HOME/.local/share/ridzgangs"
BIN="$HOME/bin"
CONFIG="$HOME/.config/ridzgangs"

echo "=================================="
echo "      RIDZGANGS FOTOAI"
echo "          INSTALLER"
echo "=================================="

pkg update -y
pkg install -y git python nano

mkdir -p "$HOME/.local/share" "$BIN" "$CONFIG"
mkdir -p "$HOME/storage/shared/DCIM/Camera"
mkdir -p "$HOME/storage/shared/DCIM/Camera_Enhanced"

if [ -d "$PROJECT/.git" ]; then
    git -C "$PROJECT" pull --ff-only
else
    git clone "$REPO" "$PROJECT"
fi

python -m pip install requests watchdog pillow

cat > "$BIN/ridzgangs" <<'LAUNCHER'
#!/data/data/com.termux/files/usr/bin/bash
PROJECT="$HOME/.local/share/ridzgangs"
CONFIG="$HOME/.config/ridzgangs"
KEYFILE="$CONFIG/key.sh"

mkdir -p "$CONFIG"
chmod 700 "$CONFIG"

if [ ! -s "$KEYFILE" ]; then
    echo "Masukkan API key OpenAI milikmu."
    read -rsp "API key: " API_KEY
    echo
    if [ -z "$API_KEY" ]; then
        echo "API key tidak boleh kosong."
        exit 1
    fi
    umask 077
    printf 'export OPENAI_API_KEY=%q\n' "$API_KEY" > "$KEYFILE"
    unset API_KEY
fi

source "$KEYFILE"
export OPENAI_API_KEY

while true; do
    clear
    echo "=================================="
    echo "       RYDZGANGS FOTOAI"
    echo "=================================="
    echo "[1] Jalankan AI Kamera"
    echo "[2] Ganti Prompt AI"
    echo "[3] Ganti API Key"
    echo "[0] Keluar"
    echo
    read -rp "Pilih menu: " PILIHAN

    case "$PILIHAN" in
        1)
            cd "$PROJECT"
            python "$PROJECT/watch_camera.py"
            read -rp "Tekan Enter untuk kembali..."
            ;;
        2)
            nano "$PROJECT/prompt.txt"
            ;;
        3)
            read -rsp "API key baru: " API_KEY
            echo
            if [ -n "$API_KEY" ]; then
                umask 077
                printf 'export OPENAI_API_KEY=%q\n' "$API_KEY" > "$KEYFILE"
                unset API_KEY
                source "$KEYFILE"
                export OPENAI_API_KEY
                echo "API key diperbarui."
            fi
            read -rp "Tekan Enter..."
            ;;
        0)
            unset OPENAI_API_KEY
            exit 0
            ;;
        *)
            echo "Pilihan tidak valid."
            sleep 1
            ;;
    esac
done
LAUNCHER

chmod 700 "$BIN/ridzgangs"

if ! grep -qF 'export PATH="$HOME/bin:$PATH"' "$HOME/.bashrc" 2>/dev/null; then
    echo 'export PATH="$HOME/bin:$PATH"' >> "$HOME/.bashrc"
fi

echo
echo "Instalasi selesai!"
echo "Jalankan: source ~/.bashrc"
echo "Lalu ketik: ridzgangs"

