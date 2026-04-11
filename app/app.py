from flask import Flask, render_template, jsonify, request
import psutil
import platform
import datetime
import re
import os
import time
import random
import json
import requests
from urllib.parse import urlparse
import socket
import ipaddress
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__, static_folder='static')

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

ALLOWED_HOSTS = {
    'crt.sh',
    'services.nvd.nist.gov',
    'bbmlab.duckdns.org',
}
ALLOWED_SCHEMES = {'https'}

def safe_fetch(url: str, timeout: int = 5):
    """Fetch sigur cu validare scheme + host. Blocheaza file://, gopher://, SSRF."""
    parsed = urlparse(url)
    if parsed.scheme not in ALLOWED_SCHEMES:
        raise ValueError(f"Scheme not allowed: {parsed.scheme}")
    if parsed.hostname not in ALLOWED_HOSTS:
        raise ValueError(f"Host not allowed: {parsed.hostname}")
    # Block private IPs (defense-in-depth pentru DNS rebinding)
    try:
        ip = ipaddress.ip_address(socket.gethostbyname(parsed.hostname))
        if ip.is_private or ip.is_loopback or ip.is_link_local:
            raise ValueError(f"Private IP blocked: {ip}")
    except (socket.gaierror, ValueError) as e:
        raise ValueError(f"DNS resolution failed: {e}")

    response = requests.get(
        url,
        timeout=timeout,
        allow_redirects=False,
        headers={'User-Agent': 'BBM-Lab-Security-Scanner/1.0'}
    )
    response.raise_for_status()
    return response

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

# ... [AICI RAMAN EXACT LA FEL RUTELE VECHI: /api/threats, /api/analyze, /api/traffic, /health] ...

@app.route('/api/threats')
def threats():
    LOG_PATH = '/app/host_auth.log'
    TAIL_LINES = 50
    MAX_RESULTS = 5
    ATTACK_KEYWORDS = re.compile(r'Failed password|Invalid user|Ban', re.IGNORECASE)
    IP_PATTERN = re.compile(r'(\d{1,3}\.\d{1,3})\.\d{1,3}\.\d{1,3}')
    USER_PATTERN = re.compile(r'((?:password|user)\s+(?:for\s+))\S+', re.IGNORECASE)

    if not os.path.isfile(LOG_PATH):
        return jsonify({'threats': [], 'source': LOG_PATH, 'status': 'file_not_found'})

    try:
        with open(LOG_PATH, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
    except (PermissionError, OSError) as e:
        return jsonify({'threats': [], 'source': LOG_PATH, 'status': str(e)})

    tail = lines[-TAIL_LINES:] if len(lines) > TAIL_LINES else lines
    masked_threats = []
    for raw_line in tail:
        line = raw_line.strip()
        if not line or not ATTACK_KEYWORDS.search(line):
            continue
        line = IP_PATTERN.sub(r'\1.***.***', line)
        line = USER_PATTERN.sub(r'\1[REDACTED]', line)
        masked_threats.append(line)

    return jsonify({
        'threats': masked_threats[-MAX_RESULTS:],
        'total_scanned': len(tail),
        'total_matched': len(masked_threats),
        'source': LOG_PATH
    })

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

@app.route('/api/proxy/headers')
@limiter.limit("10 per minute")
def proxy_headers():
    target_url = request.args.get('url', '').strip()
    if not target_url:
        return jsonify({'error': 'url param required'}), 400
    parsed = urlparse(target_url)
    if parsed.hostname != 'bbmlab.duckdns.org':
        return jsonify({'error': 'only bbmlab.duckdns.org allowed'}), 403
    try:
        response = safe_fetch(target_url, timeout=5)
        headers = dict(response.headers)
        score = 100
        # Check specific headers
        sts = headers.get('Strict-Transport-Security')
        csp = headers.get('Content-Security-Policy')
        xfo = headers.get('X-Frame-Options')
        rp = headers.get('Referrer-Policy')
        grade = "A"
        if not sts: score -= 20
        if not csp: score -= 30
        if not xfo: score -= 10
        if not rp: score -= 10
        if score >= 90: grade = "A"
        elif score >= 70: grade = "B"
        elif score >= 50: grade = "C"
        elif score >= 30: grade = "D"
        else: grade = "F"
        return jsonify({"url": target_url, "headers": headers, "score": score, "grade": grade})
    except ValueError as e:
        return jsonify({'error': str(e), 'grade': 'F'}), 400
    except requests.RequestException as e:
        return jsonify({'error': 'upstream fetch failed', 'grade': 'F'}), 502

@app.route('/api/proxy/crt')
def proxy_crt():
    domain = request.args.get('domain', 'bbmlab.duckdns.org')
    try:
        url = f"https://crt.sh/?q={domain}&output=json"
        response = safe_fetch(url, timeout=5)
        data = response.json()
        return jsonify(data)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except requests.RequestException as e:
        return jsonify({'error': 'upstream fetch failed'}), 502

@app.route('/api/proxy/nvd')
def proxy_nvd():
    keyword = request.args.get('keyword', 'docker')
    try:
        url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={keyword}&resultsPerPage=5"
        response = safe_fetch(url, timeout=10)
        data = response.json()
        return jsonify(data)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except requests.RequestException as e:
        return jsonify({'error': 'upstream fetch failed'}), 502

@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) # nosemgrep
