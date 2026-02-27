# File: blink.py
from gpiozero import LED, Device
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# PENTING: Beri tahu script ini untuk menggunakan pigpiod juga
Device.pin_factory = PiGPIOFactory(host='localhost')

# Inisialisasi LED di GPIO 4
led_merah = LED(4)

print("Memulai program blink pada GPIO 4...")
print("Cek dashboard web Anda, indikator GPIO 4 akan ikut berkedip!")
print("Tekan Ctrl+C untuk berhenti.")

try:
    while True:
        led_merah.on()
        sleep(1)
        led_merah.off()
        sleep(1)
except KeyboardInterrupt:
    print("Program dihentikan.")