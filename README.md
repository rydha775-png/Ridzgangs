# FotoAI Tools

Tools Android berbasis Termux untuk memproses foto menggunakan OpenAI.

## Fitur
- Memantau folder kamera Android.
- Mengirim foto baru ke OpenAI untuk diedit.
- Menyimpan hasil ke DCIM/Camera_Enhanced.
- Menyalin hasil AI ke DCIM/Camera agar muncul di Galeri.
- Menghapus foto asli hanya setelah hasil AI berhasil disimpan.

## Persyaratan
- Android dengan Termux.
- Python dan dependensi proyek.
- API key OpenAI milik pengguna sendiri.
- Izin penyimpanan Android.

## Instalasi
1. Unduh atau klon repositori ini.
2. Masuk ke folder proyek.
3. Jalankan:

   bash install.sh

4. Siapkan perintah fotoai sesuai panduan pengelola proyek.
5. Atur API key secara lokal:

   fotoai setup

6. Mulai pemantauan:

   fotoai start

## Perintah
- fotoai setup
- fotoai start
- fotoai stop
- fotoai status
- fotoai log
- fotoai edit /lokasi/foto.jpg

## Keamanan
Jangan unggah API key, token, atau informasi pribadi.
Setiap pengguna harus memakai API key miliknya sendiri.
Pastikan hasil AI tersimpan sebelum foto asli dihapus.

## Catatan
Proyek ini menggunakan API OpenAI yang dapat menimbulkan biaya.
Periksa harga dan ketentuan API sebelum digunakan.
