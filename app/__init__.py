from flask import Flask, render_template, jsonify, request
import re, os, random

from .extensions import limiter
from .modules.proxies import proxies_bp
from .modules.github_feed import github_bp
from .modules.sbom import sbom_bp
from .modules.threats import threats_bp
from .modules.compliance import compliance_bp
from .modules.telemetry import telemetry_bp
from .modules.uptime import uptime_bp

def create_app():
    app = Flask(__name__, static_folder='static')

    # Initialize extensions
    limiter.init_app(app)

    # Register blueprints
    app.register_blueprint(proxies_bp)
    app.register_blueprint(github_bp)
    app.register_blueprint(sbom_bp)
    app.register_blueprint(threats_bp)
    app.register_blueprint(compliance_bp)
    app.register_blueprint(telemetry_bp)
    app.register_blueprint(uptime_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

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

    @app.route('/api/health')
    def health():
        return jsonify({'status': 'ok', 'service': 'bbmlab', 'version': '1.0', 'timestamp': time()}), 200

    return app
