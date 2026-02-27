# GPIOweb Dashboard
### by @Irfan_TuxZ [ig](https://www.instagram.com/irfan_tuxz)
_(English version below)_

Dashboard GPIO Real-Time berbasis Web untuk Raspberry Pi.
Aplikasi ini menyediakan antarmuka interaktif untuk memonitor dan mengontrol pin GPIO menggunakan **Flask, WebSockets, dan `gpiozero`**. 

Sistem ini secara otomatis mendeteksi model Raspberry Pi Anda dan mengonfigurasi *backend* yang sesuai (`lgpio` untuk Raspberry Pi 5, dan `pigpiod` untuk Raspberry Pi 4 dan versi lebih lama).

## Cara Instalasi
> [!TIP]
>Jalankan perintah berikut di **terminal** Raspberry Pi Anda untuk mengunduh dan menginstal _service_ **GPIOweb**:

```bash
# Unduh repositori
wget https://github.com/irfantuxz/gpioweb/archive/refs/heads/master.zip -O gpioweb-master.zip

# Ekstrak file
unzip gpioweb-master.zip
cd gpioweb-main

# Jalankan script instalasi (membutuhkan akses sudo)
sudo bash setup.sh
```

## Cara Akses GPIOweb
Setelah terinstal dan berjalan, buka web browser dan akses alamat berikut:

> [!TIP]
> - Akses Lokal (langsung di dalam **OS Raspi**): **`http://localhost:5000`**
> - Akses Jaringan (dari **PC/Smartphone/Perangkat lain**): **`http://<IP_RASPBERRY_PI_ANDA>:5000`**

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

Skrip ini juga akan mendaftarkan GPIOweb sebagai _system daemon service_, sehingga aplikasi web ini akan berjalan otomatis di latar belakang (_background_) setiap kali Raspberry Pi dihidupkan.

_Perintah Manajemen Service:_
Anda dapat mengontrol service GPIOweb menggunakan perintah standar `systemctl`:

```Bash
sudo systemctl status gpioweb
sudo systemctl start gpioweb
sudo systemctl stop gpioweb
sudo systemctl restart gpioweb
```

# GPIOweb Dashboard (English)
Web-based Real-Time GPIO Dashboard for Raspberry Pi. This application provides an interactive UI to monitor and control GPIO pins using **Flask, WebSockets, and `gpiozero`.**

It automatically detects your Raspberry Pi model and configures the appropriate backend (`lgpio` for _Raspberry Pi 5_, and `pigpiod` for _Raspberry Pi 4 and older_).

## How to Install
> [!TIP]
>Run the following commands in your Raspberry Pi _**terminal**_ to download and install the GPIOweb service:

```Bash
# Download the repository
wget https://github.com/irfantuxz/gpioweb/archive/refs/heads/master.zip -O gpioweb-master.zip

# Extract the archive
unzip gpioweb-master.zip
cd gpioweb-main

# Run the setup script (requires sudo privileges)
sudo bash setup.sh
```

## How to Access GPIOweb
Once installed and running, open a web browser and navigate to:

> [!TIP]
> - Local Access (from RaspberryPi): **`http://localhost:5000`**
> - Network Access (from PC/other devices): **`http://<YOUR_RASPBERRY_PI_IP>:5000`**

## Included Examples
This repository includes Python test scripts to demonstrate `gpiozero` integration alongside the **GPIOweb dashboard**:

- `python test-example.py`
A simple script using gpiozero.
(Note: The downside of this basic approach is that it will cause the IO state to revert to INPUT after the script closes).

- `python blinkled-example.py`
An advanced gpiozero script using the `pigpiod` backend. It ensures the state is properly closed and returns the IO to a LOW state upon exit.

## How It Works
The `setup.sh` script automatically detects your hardware and installs the necessary packages:

- `lgpio` is installed for **Raspberry Pi 5**.
- `pigpio` daemon is compiled and installed for **Raspberry Pi 1, 2, 3, and 4**.

The script will also register **_GPIOweb_** as a _system daemon service_, allowing it to run automatically in the background on boot.

Service Management Commands:
You can manage the GPIOweb service using standard systemctl commands:

```Bash
sudo systemctl status gpioweb
sudo systemctl start gpioweb
sudo systemctl stop gpioweb
sudo systemctl restart gpioweb
```
