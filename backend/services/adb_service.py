import subprocess
import shutil
import json

def _run_cmd(cmd):
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=False, text=True)
        return output
    except FileNotFoundError:
        return None
    except subprocess.CalledProcessError as e:
        return e.output

def check_adb_connection():
    if not shutil.which('adb'):
        return {'error': 'ADB not found. Please install Android Platform Tools and add ADB to PATH.'}
    out = _run_cmd(['adb', 'version'])
    return {'adb_version': out.strip() if out else 'unknown'}

def detect_devices():
    if not shutil.which('adb'):
        return {'error': 'ADB not found. Please install Android Platform Tools and add ADB to PATH.'}
    out = _run_cmd(['adb', 'devices', '-l'])
    if not out:
        return {'devices': []}
    lines = out.strip().splitlines()
    devices = []
    for line in lines[1:]:
        if not line.strip():
            continue
        parts = line.split()
        if parts[1] == 'device':
            devices.append({'id': parts[0], 'info': ' '.join(parts[2:])})
    return {'devices': devices}

def get_device_info(device_id: str):
    if not shutil.which('adb'):
        return {'error': 'ADB not found. Please install Android Platform Tools and add ADB to PATH.'}
    props = {}
    for prop in ['ro.product.manufacturer', 'ro.product.model', 'ro.build.version.release']:
        out = _run_cmd(['adb', '-s', device_id, 'shell', 'getprop', prop])
        props[prop] = out.strip() if out else None
    return {
        'device_id': device_id,
        'manufacturer': props.get('ro.product.manufacturer'),
        'model': props.get('ro.product.model'),
        'android_version': props.get('ro.build.version.release')
    }
