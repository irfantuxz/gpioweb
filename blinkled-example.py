# File: blink.py
from gpiozero import LED, Device
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# PENTING: Beri tahu script ini untuk menggunakan pigpiod juga
Device.pin_factory = PiGPIOFactory(host='localhost')

# Inisialisasi LED di GPIO 4
led1 = LED(4)

print("Memulai program blink pada GPIO 4...")
print("Cek dashboard web Anda, indikator GPIO 4 akan ikut berkedip!")
print("Tekan Ctrl+C untuk berhenti.")

try:
    while True:
        led1.on()
        sleep(1)
        led1.off()
        sleep(1)
except KeyboardInterrupt:
    led1.off()
    print("Program dihentikan.")
