from flask import Blueprint, jsonify

compliance_bp = Blueprint('compliance', __name__)

FRAMEWORKS = {
    'cis_docker': {
        'name': 'CIS Docker Benchmark',
        'controls': [
            {'id': '1.1', 'name': 'Separate partition for containers', 'passed': True},
            {'id': '2.1', 'name': 'Restrict network traffic between containers', 'passed': True},
            {'id': '4.1', 'name': 'Container runs as non-root user', 'passed': True},
            {'id': '4.5', 'name': 'No secrets in Dockerfile', 'passed': True},
            {'id': '4.6', 'name': 'HEALTHCHECK instruction added', 'passed': True},
            {'id': '5.10', 'name': 'Memory usage limited', 'passed': True},
            {'id': '5.12', 'name': 'Root filesystem mounted read-only', 'passed': False},
            {'id': '5.25', 'name': 'Container restricted from acquiring privileges', 'passed': True},
        ]
    },
    'owasp_top10': {
        'name': 'OWASP Top 10 (2021)',
        'controls': [
            {'id': 'A01', 'name': 'Broken Access Control', 'passed': True},
            {'id': 'A02', 'name': 'Cryptographic Failures (TLS 1.3)', 'passed': True},
            {'id': 'A03', 'name': 'Injection (parameterized queries)', 'passed': True},
            {'id': 'A04', 'name': 'Insecure Design (threat modeling)', 'passed': True},
            {'id': 'A05', 'name': 'Security Misconfiguration', 'passed': True},
            {'id': 'A06', 'name': 'Vulnerable Components (Trivy scan)', 'passed': True},
            {'id': 'A07', 'name': 'Auth Failures (rate limiting)', 'passed': True},
            {'id': 'A08', 'name': 'Software Integrity (SRI hashes)', 'passed': True},
            {'id': 'A09', 'name': 'Logging & Monitoring', 'passed': True},
            {'id': 'A10', 'name': 'SSRF Protection (allowlist)', 'passed': True},
        ]
    },
    'nist_csf': {
        'name': 'NIST Cybersecurity Framework',
        'controls': [
            {'id': 'ID', 'name': 'Identify — Asset inventory (SBOM)', 'passed': True},
            {'id': 'PR.AC', 'name': 'Protect — Access Control', 'passed': True},
            {'id': 'PR.DS', 'name': 'Protect — Data Security (encryption)', 'passed': True},
            {'id': 'PR.IP', 'name': 'Protect — Info Protection Processes', 'passed': True},
            {'id': 'DE.CM', 'name': 'Detect — Continuous Monitoring', 'passed': True},
            {'id': 'DE.AE', 'name': 'Detect — Anomalies & Events', 'passed': False},
            {'id': 'RS.RP', 'name': 'Respond — Response Planning', 'passed': True},
            {'id': 'RC.RP', 'name': 'Recover — Recovery Planning', 'passed': True},
        ]
    }
}

@compliance_bp.route('/api/compliance')
def compliance():
    result = {}
    for key, fw in FRAMEWORKS.items():
        passed = sum(1 for c in fw['controls'] if c['passed'])
        total = len(fw['controls'])
        result[key] = {
            'name': fw['name'],
            'passed': passed,
            'total': total,
            'percentage': round(passed / total * 100),
            'controls': fw['controls'],
        }
    return jsonify(result)
