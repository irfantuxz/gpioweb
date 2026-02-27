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

# Definisi Warna
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color (Reset ke default)

echo "========================================="
echo -e "${GREEN}Instalasi Selesai!${NC}"
echo -e "Contoh ${YELLOW}python blinkled-example.py${NC}"
echo -e "Contoh ${YELLOW}python test-example.py${NC}"
echo "========================================="
echo -e "${BOLD}Status service GPIOweb:${NC}"
systemctl is-active gpioweb
echo -e "Silakan akses dashboard GPIOweb di ${CYAN}http://localhost:5000${NC}"
echo -e "Atau lewat PC/HP local network di ${CYAN}http://ALAMAT_IP_RASPI:5000${NC}"
echo "========================================="
