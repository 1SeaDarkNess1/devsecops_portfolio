from flask import Flask, render_template, jsonify
import psutil
import platform
import datetime
import re
import os

app = Flask(__name__)

def bytes_to_gb(b):
    """Convert bytes to gigabytes and round to 2 decimal places."""
    return round(b / 1024 / 1024 / 1024, 2)

def bytes_to_mb(b):
    """Convert bytes to megabytes and round to 2 decimal places."""
    return round(b / 1024 / 1024, 2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/metrics')
def metrics():
    # CPU
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count()
    
    # RAM
    ram = psutil.virtual_memory()
    
    # Disk
    disk = psutil.disk_usage('/')
    
    # Network
    net = psutil.net_io_counters()
    
    # Uptime
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.datetime.now() - boot_time
    hours, remainder = divmod(int(uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    
    return jsonify({
        'cpu': {
            'percent': cpu_percent,
            'cores': cpu_count
        },
        'ram': {
            'total': bytes_to_gb(ram.total),
            'used': bytes_to_gb(ram.used),
            'percent': ram.percent
        },
        'disk': {
            'total': bytes_to_gb(disk.total),
            'used': bytes_to_gb(disk.used),
            'percent': disk.percent
        },
        'network': {
            'bytes_sent': bytes_to_mb(net.bytes_sent),
            'bytes_recv': bytes_to_mb(net.bytes_recv)
        },
        'uptime': f'{hours}h {minutes}m {seconds}s',
        'hostname': platform.node(),
        'os': platform.system() + ' ' + platform.release()
    })

@app.route('/api/threats')
def threats():
    """Read, filter, and obfuscate security logs from auth.log."""
    LOG_PATH = '/app/host_auth.log'
    TAIL_LINES = 50
    MAX_RESULTS = 5
    ATTACK_KEYWORDS = re.compile(
        r'Failed password|Invalid user|Ban', re.IGNORECASE
    )
    # Matches standard IPv4 addresses
    IP_PATTERN = re.compile(
        r'(\d{1,3}\.\d{1,3})\.\d{1,3}\.\d{1,3}'
    )
    # Matches 'for <username>' after 'password' or 'user'
    USER_PATTERN = re.compile(
        r'((?:password|user)\s+(?:for\s+))\S+', re.IGNORECASE
    )

    # --- Read log file ---
    if not os.path.isfile(LOG_PATH):
        return jsonify({'threats': [], 'source': LOG_PATH, 'status': 'file_not_found'})

    try:
        with open(LOG_PATH, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
    except (PermissionError, OSError) as e:
        return jsonify({'threats': [], 'source': LOG_PATH, 'status': str(e)})

    # Take last N lines
    tail = lines[-TAIL_LINES:] if len(lines) > TAIL_LINES else lines

    # --- Filter & obfuscate ---
    masked_threats = []
    for raw_line in tail:
        line = raw_line.strip()
        if not line or not ATTACK_KEYWORDS.search(line):
            continue

        # Mask IP: keep first 2 octets, replace last 2 with ***
        line = IP_PATTERN.sub(r'\1.***.***', line)

        # Redact username
        line = USER_PATTERN.sub(r'\1[REDACTED]', line)

        masked_threats.append(line)

    # Return only the most recent MAX_RESULTS entries
    return jsonify({
        'threats': masked_threats[-MAX_RESULTS:],
        'total_scanned': len(tail),
        'total_matched': len(masked_threats),
        'source': LOG_PATH
    })

@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) # nosemgrep
