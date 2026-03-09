from flask import Flask, render_template, request
from flask_socketio import SocketIO
from gpiozero import DigitalOutputDevice, InputDevice, pi_info, Device
from gpiozero.pins.pigpio import PiGPIOFactory
import time

try:
    from gpiozero.pins.lgpio import LGPIOFactory
except ImportError:
    LGPIOFactory = None

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

def get_pi_model():
    try:
        with open('/sys/firmware/devicetree/base/model', 'r') as f:
            return f.read().strip('\x00')
    except Exception:
        return "Raspberry Pi (Unknown Model)"

model_name = get_pi_model()

# --- Auto-Select Backend ---
if "Raspberry Pi 5" in model_name and LGPIOFactory is not None:
    Device.pin_factory = LGPIOFactory()
else:
    try:
        Device.pin_factory = PiGPIOFactory(host='localhost')
    except:
        pass

gpio_active_devices = {}

def get_or_create_device(bcm, mode="output", pull=None):
    # """Fungsi untuk mengambil kontrol pin secara dinamis"""
    if bcm in gpio_active_devices:
        gpio_active_devices[bcm].close()
    
    if mode == "output":
        gpio_active_devices[bcm] = DigitalOutputDevice(bcm)
    else:
        # pull 'up', pull 'down', atau None
        gpio_active_devices[bcm] = InputDevice(bcm, pull_up=(pull == 'up'))
    return gpio_active_devices[bcm]

@app.route('/')
def index():
    return render_template('index.html', model_name=model_name)

def background_thread():
    # """Monitoring mode menggunakan pin_factory (Non-blocking)"""
    while True:
        status = {}
        for bcm in range(2, 28): # Scan BCM 2-27
            try:
                # Menggunakan pin_factory secara langsung untuk membaca status tanpa "mengunci" pin
                raw_pin = Device.pin_factory.pin(bcm)
                mode = raw_pin.function
                
                # Deteksi Pull Status (bergantung pada kemampuan backend factory)
                pull = "FLOAT"
                try:
                    # Pada banyak factory, kita bisa mengecek pull lewat internal state
                    pull = raw_pin.pull
                except: pass

                status[bcm] = {
                    'value': raw_pin.state,
                    'mode': mode.upper(),
                    'pull': pull.upper() if pull else "NONE"
                }
                # Jangan lupa tutup handle raw_pin agar tidak leak
                raw_pin.close()
            except:
                continue
                
        socketio.emit('status_update', status)
        socketio.sleep(0.1)

@socketio.on('toggle_action')
def handle_toggle(data):
    # """Klik Kiri: Toggle Value (Output) atau Toggle Pull (Input)"""
    bcm = data.get('bcm')
    current_mode = data.get('mode').lower()
    
    if current_mode == 'output':
        dev = get_or_create_device(bcm, mode='output')
        dev.toggle()
    else:
        # Jika input, toggle antara Pull Up dan Pull Down
        current_pull = data.get('pull').lower()
        new_pull = 'down' if current_pull == 'up' else 'up'
        get_or_create_device(bcm, mode='input', pull=new_pull)

@socketio.on('change_mode')
def handle_change_mode(data):
    # """Klik Kanan: Switch antara Input dan Output"""
    bcm = data.get('bcm')
    target_mode = 'input' if data.get('current_mode').lower() == 'output' else 'output'
    get_or_create_device(bcm, mode=target_mode)

@socketio.on('release_all')
def release_all():
    # """Dijalankan saat Write Mode dimatikan di UI: Melepas semua kuncian pin"""
    global gpio_active_devices
    for bcm in list(gpio_active_devices.keys()):
        gpio_active_devices[bcm].close()
        del gpio_active_devices[bcm]
    print("Semua GPIO dilepaskan (Monitoring Mode Only)")

if __name__ == '__main__':
    socketio.start_background_task(background_thread)
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
