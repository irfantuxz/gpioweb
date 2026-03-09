import RPi.GPIO as GPIO
from time import sleep

# Konfigurasi pin
GPIO.setmode(GPIO.BCM)    # Gunakan penomoran BCM
GPIO.setup(17, GPIO.OUT)  # BCM 17, Physical 11

try:
    while True:
        GPIO.output(17, GPIO.HIGH)  # LED ON
        sleep(1)
        GPIO.output(17, GPIO.LOW)   # LED OFF
        sleep(1)
      
except KeyboardInterrupt:
    print("Program dihentikan")

finally:
    GPIO.cleanup()  # Reset semua pin GPIO
