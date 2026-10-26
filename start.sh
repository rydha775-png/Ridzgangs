
#!/data/data/com.termux/files/usr/bin/bash

PROJECT="$HOME/foto-ai"
PROMPT="$PROJECT/prompt.txt"

while true; do
  clear
  echo "======================================"
  echo "          RIDZGANGS FOTOAI"
  echo "       AI CAMERA AUTOMATION"
  echo "======================================"
  echo
  echo "  [1] Jalankan AI Kamera"
  echo "  [2] Ganti Prompt AI"
  echo "  [0] Keluar"
  echo
  read -rp "Pilih menu: " pilihan

  case "$pilihan" in
    1)
      echo
      echo "Memulai AI Camera..."
      cd "$PROJECT" || exit 1
      python "$PROJECT/watch_camera.py"
      read -rp "Tekan Enter untuk kembali ke menu..."
      ;;

    2)
      echo
      echo "Membuka editor prompt AI..."
      sleep 1

      nano "$PROMPT"

      echo
      echo "Editor ditutup."
      echo "Prompt tersimpan jika kamu menekan Ctrl+O lalu Enter."
      echo "Perubahan akan digunakan pada foto berikutnya."
      read -rp "Tekan Enter untuk kembali ke menu..."
      ;;

    0)
      echo "Terima kasih telah menggunakan Ridzgangs FotoAI."
      exit 0
      ;;
    *)
      echo "Pilihan tidak valid."
      sleep 1
      ;;
  esac
done

