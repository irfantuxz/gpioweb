from flask import Flask, render_template
from flask_socketio import SocketIO
from gpiozero import DigitalOutputDevice, pi_info, Device
from gpiozero.pins.pigpio import PiGPIOFactory
import time

# Import lgpio, bypass jika tidak tersedia di sistem
try:
    from gpiozero.pins.lgpio import LGPIOFactory
except ImportError:
    LGPIOFactory = None

app = Flask(__name__)
# Inisialisasi WebSocket
socketio = SocketIO(app, cors_allowed_origins="*")

def get_pi_model():
    try:
        with open('/sys/firmware/devicetree/base/model', 'r') as f:
            return f.read().strip('\x00')
    except Exception:
        return "Raspberry Pi (Unknown Model)"

model_name = get_pi_model()

# --- Auto-Select Backend (lgpio untuk Pi 5, pigpiod untuk lainnya) ---
if "Raspberry Pi 5" in model_name and LGPIOFactory is not None:
    Device.pin_factory = LGPIOFactory()
    print("Backend: lgpio (Raspberry Pi 5 terdeteksi)")
else:
    try:
        Device.pin_factory = PiGPIOFactory(host='localhost')
        print("Backend: pigpiod")
    except Exception as e:
        print(f"Gagal inisialisasi pigpiod: {e}")

bcm_pins = [
    2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 
    16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27
]

gpio_devices = {}

for pin in bcm_pins:
    try:
        gpio_devices[pin] = DigitalOutputDevice(pin)
    except Exception as e:
        print(f"Gagal inisialisasi BCM {pin}: {e}")

@app.route('/')
def index():
    try:
        info = pi_info()
        soc_name = info.soc
        ram_size = f"{info.memory}MB" if info.memory < 1024 else f"{info.memory // 1024}GB"
    except Exception:
        soc_name = "Unknown SoC"
        ram_size = "Unknown RAM"

    return render_template('index.html', model_name=model_name, soc_name=soc_name, ram_size=ram_size)

# --- Background Thread WebSocket ---
def background_thread():
    """Loop membaca status hardware murni lalu dikirim otomatis ke semua klien via WebSocket"""
    while True:
        status = {pin: device.value for pin, device in gpio_devices.items()}
        socketio.emit('status_update', status)
        socketio.sleep(0.1) # Kecepatan refresh 100ms

@socketio.on('connect')
def handle_connect():
    pass # Status pertama otomatis terkirim dari background_thread

@socketio.on('toggle')
def handle_toggle(data):
    bcm_pin = data.get('bcm')
    write_mode = data.get('write_mode', False)
    
    if write_mode and bcm_pin in gpio_devices:
        device = gpio_devices[bcm_pin]

        try:
            # CEK LAPIS 1: Cek dan paksa mode ke OUTPUT secara dinamis
            # Ini sangat berguna jika script eksternal (seperti testled) mengubahnya jadi INPUT
            if device.pin.function != 'output':
                print(f"Pin {bcm_pin} berubah jadi input! Memaksa kembali ke output...")
                device.pin.function = 'output'

            # Eksekusi perubahan status
            device.toggle()

        except Exception as e:
            print(f"Error fatal pada pin {bcm_pin}: {e}. Melakukan reset objek...")

            # CEK LAPIS 2: Re-inisialisasi bersih jika Lapis 1 gagal
            try:
                # Lepaskan ikatan objek lama agar TIDAK terjadi GPIOPinInUse
                device.close() 
            except Exception:
                pass

            # Buat objek baru (otomatis mengatur ulang ke Output)
            new_device = DigitalOutputDevice(bcm_pin)
            gpio_devices[bcm_pin] = new_device
            new_device.toggle()

if __name__ == '__main__':
    # Mulai broadcast status di background
    socketio.start_background_task(background_thread)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=False, allow_unsafe_werkzeug=True)
