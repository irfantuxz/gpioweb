# GPIOweb Dashboard
*(English version below)*

Dashboard GPIO Real-Time berbasis Web untuk Raspberry Pi. Aplikasi ini menyediakan antarmuka interaktif untuk memonitor dan mengontrol pin GPIO menggunakan Flask, WebSockets, dan `gpiozero`. 

Sistem ini secara otomatis mendeteksi model Raspberry Pi Anda dan mengonfigurasi *backend* yang sesuai (`lgpio` untuk Raspberry Pi 5, dan `pigpiod` untuk Raspberry Pi 4 dan versi lebih lama).

## Cara Instalasi

Jalankan perintah berikut di terminal Raspberry Pi Anda untuk mengunduh dan menginstal *service* GPIOweb:

```bash
# Unduh repositori
wget [https://github.com/irfantuxz/gpioweb/archive/refs/heads/master.zip](https://github.com/irfantuxz/gpioweb/archive/refs/heads/master.zip) -O gpioweb.zip

# Ekstrak file
unzip gpioweb.zip
cd gpioweb-master

# Jalankan script instalasi (membutuhkan akses sudo)
sudo bash setup.sh
```

