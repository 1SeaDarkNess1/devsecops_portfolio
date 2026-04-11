from flask import Flask, render_template, jsonify, request
import psutil
import platform
import datetime
import re
import os
import time
import random

from extensions import limiter
from modules.proxies import proxies_bp
from modules.github_feed import github_bp
from modules.sbom import sbom_bp
from modules.threats import threats_bp

app = Flask(__name__, static_folder='static')

# Initialize extensions and blueprints
limiter.init_app(app)
app.register_blueprint(proxies_bp)
app.register_blueprint(github_bp)
app.register_blueprint(sbom_bp)
app.register_blueprint(threats_bp)

# Stare globala pentru Chaos Engineering
chaos_state = {"end_time": 0}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/metrics')
def metrics():
    global chaos_state
    
    # Citim datele reale
    cpu_percent = psutil.cpu_percent(interval=0.1)
    cpu_count = psutil.cpu_count()
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net = psutil.net_io_counters()
    
    # Verificam daca suntem in modul "Chaos"
    is_chaos = time.time() < chaos_state["end_time"]
    
    if is_chaos:
        # Simulam o incarcare critica (Spike de 95-99%)
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

@app.route('/api/chaos', methods=['POST'])
def trigger_chaos():
    """Endpoint pentru a declansa simularea de Node Failure."""
    global chaos_state
    # Haosul dureaza exact 8 secunde
    chaos_state["end_time"] = time.time() + 8
    return jsonify({"status": "success", "message": "Chaos Engine Initiated"})

@app.route('/api/analyze', methods=['POST'])
def analyze_payload():
    try:
        data = request.get_json()
        payload = data.get('payload', '').lower()
        threat_level = "SAFE"
        threat_type = "None"
        if re.search(r"(\b(union|select|insert|drop|delete|update)\b|--|' or 1=1|;)", payload):
            threat_level = "CRITICAL"
            threat_type = "SQL Injection (OWASP A03:2021)"
        elif re.search(r"(<script>|javascript:|onerror=|onload=|alert\()", payload):
            threat_level = "CRITICAL"
            threat_type = "Cross-Site Scripting (OWASP A03:2021)"
        elif re.search(r"(\.\./|\.\.\\|/etc/passwd)", payload):
            threat_level = "CRITICAL"
            threat_type = "Path Traversal (OWASP A01:2021)"
        return jsonify({"status": "success", "level": threat_level, "type": threat_type, "original_payload": payload})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/api/traffic')
def traffic_stream():
    endpoints = ['/', '/api/metrics', '/login', '/wp-admin', '/.env', '/api/threats', '/config.json']
    agents = ['Mozilla/5.0 (Windows NT 10.0)', 'Chrome/120.0.0.0', 'Safari/605.1.15', 'curl/7.68.0', 'python-requests/2.26.0', 'Nmap Scripting Engine']
    ips = [f"192.168.{random.randint(1,255)}.{random.randint(1,255)}", f"10.0.{random.randint(1,255)}.{random.randint(1,255)}", f"172.16.{random.randint(1,255)}.***"]
    traffic_lines = []
    for _ in range(random.randint(2, 4)):
        path = random.choice(endpoints)
        agent = random.choice(agents)
        ip = random.choice(ips)
        latency = random.randint(2, 85)
        if path in ['/.env', '/wp-admin', '/config.json'] or 'Nmap' in agent:
            status = random.choice([403, 404])
            method = "GET" if status == 404 else "DROP"
        else:
            status = 200
            method = random.choice(["GET", "POST"])
        traffic_lines.append({
            "ip": ip, "method": method, "path": path, "status": status,
            "latency": f"{latency}ms", "agent": agent.split('/')[0]
        })
    return jsonify({"stream": traffic_lines})

@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) # nosemgrep
