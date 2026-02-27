# GPIOweb Dashboard
## by @Irfan_TuxZ [https://www.instagram.com/irfan_tuxz](ig)
*(English version below)*

Dashboard GPIO Real-Time berbasis Web untuk Raspberry Pi. Aplikasi ini menyediakan antarmuka interaktif untuk memonitor dan mengontrol pin GPIO menggunakan Flask, WebSockets, dan `gpiozero`. 

Sistem ini secara otomatis mendeteksi model Raspberry Pi Anda dan mengonfigurasi *backend* yang sesuai (`lgpio` untuk Raspberry Pi 5, dan `pigpiod` untuk Raspberry Pi 4 dan versi lebih lama).

## Cara Instalasi

Jalankan perintah berikut di terminal Raspberry Pi Anda untuk mengunduh dan menginstal *service* GPIOweb:

```bash
# Unduh repositori
wget [https://github.com/irfantuxz/gpioweb/archive/refs/heads/master.zip](https://github.com/irfantuxz/gpioweb/archive/refs/heads/master.zip) -O gpioweb-master.zip

# Ekstrak file
unzip gpioweb-master.zip
cd gpioweb-master

# Jalankan script instalasi (membutuhkan akses sudo)
sudo bash setup.sh
```

## Cara Akses GPIOweb
Setelah terinstal dan berjalan, buka web browser dan akses alamat berikut:

- Akses Lokal (di dalam Raspi): `http://localhost:5000`
- Akses Jaringan (dari PC/HP lain): `http://<IP_RASPBERRY_PI_ANDA>:5000`

## Contoh Skrip Python yang Disertakan
Repositori ini menyertakan skrip pengujian Python untuk mendemonstrasikan integrasi `gpiozero` yang berjalan berdampingan dengan dashboard GPIOweb:

- `python test-example.py`
Kode sederhana menggunakan gpiozero.
(Catatan: Kelemahan dari metode dasar ini adalah status pin IO akan berubah kembali menjadi INPUT setelah skrip ditutup/selesai).

- `python blinkled-example.py`
Skrip gpiozero tingkat lanjut yang menggunakan _backend_ `pigpiod`. Skrip ini memastikan status pin ditutup dengan benar dan mengembalikan IO ke status LOW (mati) saat skrip keluar.

## Cara Kerja Sistem
Skrip `setup.sh` akan secara otomatis mendeteksi perangkat keras Anda dan menginstal paket-paket yang dibutuhkan:

- Paket `lgpio` diinstal untuk **Raspberry Pi 5**.

- Daemon `pigpio` dikompilasi dan diinstal untuk **Raspberry Pi 1, 2, 3, dan 4.**

Skrip ini juga akan mendaftarkan GPIOweb sebagai *system daemon service*, sehingga aplikasi web ini akan berjalan otomatis di latar belakang (*background*) setiap kali Raspberry Pi dihidupkan.

*Perintah Manajemen Service:*
Anda dapat mengontrol service GPIOweb menggunakan perintah standar `systemctl`:

```Bash
sudo systemctl status gpioweb
sudo systemctl start gpioweb
sudo systemctl stop gpioweb
sudo systemctl restart gpioweb
```

# GPIOweb Dashboard (English)
Web-based Real-Time GPIO Dashboard for Raspberry Pi. This application provides an interactive UI to monitor and control GPIO pins using Flask, WebSockets, and gpiozero.

It automatically detects your Raspberry Pi model and configures the appropriate backend (lgpio for Raspberry Pi 5, and pigpiod for Raspberry Pi 4 and older).

How to Install
Run the following commands in your Raspberry Pi terminal to download and install the GPIOweb service:

Bash
# Download the repository
wget [https://github.com/irfantuxz/gpioweb/archive/refs/heads/master.zip](https://github.com/irfantuxz/gpioweb/archive/refs/heads/master.zip) -O gpioweb.zip

# Extract the archive
unzip gpioweb.zip
cd gpioweb-master

# Run the setup script (requires sudo privileges)
sudo bash setup.sh
How to Access GPIOweb
Once installed and running, open a web browser and navigate to:

Local Access: http://localhost:5000

Network Access: http://<YOUR_RASPBERRY_PI_IP>:5000

Included Examples
This repository includes Python test scripts to demonstrate gpiozero integration alongside the GPIOweb dashboard:

python test-example.py
A simple script using gpiozero.
(Note: The downside of this basic approach is that it will cause the IO state to revert to INPUT after the script closes).

python blinkled-example.py
An advanced gpiozero script using the pigpiod backend. It ensures the state is properly closed and returns the IO to a LOW state upon exit.

How It Works
The setup.sh script automatically detects your hardware and installs the necessary packages:

lgpio is installed for Raspberry Pi 5.

pigpio daemon is compiled and installed for Raspberry Pi 1, 2, 3, and 4.

The script will also register GPIOweb as a system daemon service, allowing it to run automatically in the background on boot.

Service Management Commands:
You can manage the GPIOweb service using standard systemctl commands:

Bash
sudo systemctl status gpioweb
sudo systemctl start gpioweb
sudo systemctl stop gpioweb
sudo systemctl restart gpioweb

---

### 2. Simpan sebagai `setup.sh`

```bash
#!/bin/bash

# Pastikan script dijalankan sebagai root/sudo
if [ "$EUID" -ne 0 ]; then
  echo "Harap jalankan script ini dengan sudo: sudo bash setup.sh"
  exit 1
fi

APP_DIR=$PWD
echo "Memulai instalasi GPIOweb di direktori: $APP_DIR"

# 1. Update sistem dan instal dependensi dasar via APT
echo "Menginstal paket dasar APT..."
apt update
apt install -y python3-flask python3-gpiozero python3-pip build-essential unzip

# Deteksi Model Raspberry Pi
PI_MODEL=$(cat /sys/firmware/devicetree/base/model | tr -d '\0')
echo "Sistem mendeteksi: $PI_MODEL"

# 2. Logika Pemilihan Backend & Instalasi PIP
if [[ "$PI_MODEL" == *"Raspberry Pi 5"* ]]; then
    echo "Raspberry Pi 5 terdeteksi. Menginstal dependensi via pip..."
    # Menginstal Flask-SocketIO dan lgpio sekaligus untuk Pi 5
    pip install Flask-SocketIO lgpio --break-system-packages
    echo "Instalasi dependensi untuk Pi 5 selesai."

else
    echo "Raspberry Pi 4 atau versi lebih lama terdeteksi. Menyiapkan pigpiod..."
    
    # Instal Flask-SocketIO saja via pip (lgpio tidak wajib untuk Pi 4 ke bawah jika pakai pigpiod)
    pip install Flask-SocketIO --break-system-packages
    
    # Download, ekstrak, dan kompilasi pigpio
    echo "Mengunduh source code pigpio..."
    wget https://github.com/joan2937/pigpio/archive/master.zip -O pigpio.zip
    unzip -o pigpio.zip
    cd pigpio-master || exit
    
    echo "Kompilasi pigpio (memakan waktu sekitar 1-2 menit)..."
    make
    make install
    
    # Membuat Systemd Service untuk pigpiod
    echo "Membuat service untuk pigpiod..."
    cat << 'EOF' > /etc/systemd/system/pigpiod.service
[Unit]
Description=Pigpio Daemon Server
After=network.target

[Service]
ExecStart=/usr/local/bin/pigpiod -l
ExecStop=/bin/systemctl kill pigpiod
Type=forking
Restart=always

[Install]
WantedBy=multi-user.target
EOF

    # Aktifkan dan jalankan pigpiod
    systemctl daemon-reload
    systemctl enable pigpiod
    systemctl start pigpiod
    
    # Kembali ke direktori aplikasi
    cd "$APP_DIR"
    echo "Instalasi pigpiod selesai."
fi

# 3. Membuat Service untuk gpioweb.py
echo "Membuat systemd service untuk gpioweb..."

# Menggunakan nama user yang mengeksekusi sudo
CURRENT_USER=${SUDO_USER:-root}

cat << EOF > /etc/systemd/system/gpioweb.service
[Unit]
Description=GPIOweb Dashboard Service
After=network.target pigpiod.service

[Service]
User=$CURRENT_USER
WorkingDirectory=$APP_DIR
ExecStart=/usr/bin/python3 $APP_DIR/app.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# 4. Aktifkan dan jalankan service gpioweb
systemctl daemon-reload
systemctl enable gpioweb
systemctl restart gpioweb

echo "========================================="
echo "Instalasi Selesai!"
echo "Status service GPIOweb:"
systemctl is-active gpioweb
echo "Silakan akses dashboard di http://localhost:5000"
echo "========================================="
(Tips: Jika Anda mengerjakan ini langsung di dalam Raspberry Pi melalui SSH, Anda bisa membuat file dengan perintah nano README.md, lalu klik kanan untuk mem-paste isinya, tekan Ctrl+O, Enter, lalu Ctrl+X. Lakukan hal yang sama untuk nano setup.sh)
