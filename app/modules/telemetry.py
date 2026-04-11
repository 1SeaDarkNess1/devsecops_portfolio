from flask import Blueprint, jsonify
import psutil, platform, datetime, time, random

telemetry_bp = Blueprint('telemetry', __name__)

# Global state for Chaos Engineering (shared across modules if needed)
# In a real app, this might be in a shared storage or specialized module
chaos_state = {"end_time": 0}

@telemetry_bp.route('/api/metrics')
def metrics():
    global chaos_state
    
    cpu_percent = psutil.cpu_percent(interval=0.1)
    cpu_count = psutil.cpu_count()
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net = psutil.net_io_counters()
    
    is_chaos = time.time() < chaos_state["end_time"]
    
    if is_chaos:
        cpu_percent = round(random.uniform(95.5, 99.9), 1)
        ram_percent = round(random.uniform(85.0, 95.0), 1)
    else:
        ram_percent = ram.percent
        
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.datetime.now() - boot_time
    hours, remainder = divmod(int(uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    
    return jsonify({
        'cpu': {
            'percent': cpu_percent,
            'cores': cpu_count,
            'status': 'CRITICAL' if is_chaos else 'NORMAL'
        },
        'ram': {
            'total': round(ram.total / 1024 / 1024 / 1024, 2),
            'used': round(ram.used / 1024 / 1024 / 1024, 2),
            'percent': ram_percent
        },
        'disk': {
            'total': round(disk.total / 1024 / 1024 / 1024, 2),
            'used': round(disk.used / 1024 / 1024 / 1024, 2),
            'percent': disk.percent
        },
        'network': {
            'bytes_sent': round(net.bytes_sent / 1024 / 1024, 2),
            'bytes_recv': round(net.bytes_recv / 1024 / 1024, 2)
        },
        'uptime': f'{hours}h {minutes}m {seconds}s',
        'hostname': platform.node(),
        'os': platform.system() + ' ' + platform.release()
    })

@telemetry_bp.route('/api/chaos', methods=['POST'])
def trigger_chaos():
    global chaos_state
    chaos_state["end_time"] = time.time() + 8
    return jsonify({"status": "success", "message": "Chaos Engine Initiated"})
