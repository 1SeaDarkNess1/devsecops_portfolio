from flask import Blueprint, jsonify, request
import requests, socket, ipaddress, ssl
from urllib.parse import urlparse
from datetime import datetime
from time import time
from app.extensions import limiter

proxies_bp = Blueprint('proxies', __name__)

ALLOWED_HOSTS = {'crt.sh', 'services.nvd.nist.gov', 'http-observatory.security.mozilla.org', 'bbmlab.duckdns.org'}
_cache = {}  # {key: (timestamp, data)}

def safe_fetch(url, timeout=8):
    p = urlparse(url)
    if p.scheme != 'https' or p.hostname not in ALLOWED_HOSTS:
        raise ValueError(f"blocked: {url}")
    # Anti-SSRF DNS verification
    try:
        ip = ipaddress.ip_address(socket.gethostbyname(p.hostname))
        if ip.is_private or ip.is_loopback or ip.is_link_local:
            raise ValueError(f"Private IP blocked: {ip}")
    except (socket.gaierror, ValueError) as e:
        raise ValueError(f"DNS resolution failed: {e}")
        
    return requests.get(url, timeout=timeout, allow_redirects=False,
                        headers={'User-Agent': 'BBM-Lab-Security-Scanner/1.0'})

def cached(key, ttl, fn):
    now = time()
    if key in _cache and now - _cache[key][0] < ttl:
        return _cache[key][1]
    data = fn()
    _cache[key] = (now, data)
    return data

# ─── MODUL 1: Security Headers (self-scan) ───
@proxies_bp.route('/api/security/headers')
@limiter.limit("10 per minute")
def headers_scan():
    target = 'https://bbmlab.duckdns.org'
    try:
        r = safe_fetch(target, timeout=5)
        h = {k.lower(): v for k, v in r.headers.items()}
        checks = {
            'strict-transport-security': bool(h.get('strict-transport-security')),
            'content-security-policy': bool(h.get('content-security-policy')),
            'x-frame-options': bool(h.get('x-frame-options')),
            'x-content-type-options': bool(h.get('x-content-type-options')),
            'referrer-policy': bool(h.get('referrer-policy')),
            'permissions-policy': bool(h.get('permissions-policy')),
            'cross-origin-opener-policy': bool(h.get('cross-origin-opener-policy')),
            'cross-origin-resource-policy': bool(h.get('cross-origin-resource-policy')),
        }
        passed = sum(checks.values())
        score = round((passed / len(checks)) * 100)
        grade = 'A+' if score == 100 else 'A' if score >= 87 else 'B' if score >= 75 else 'C' if score >= 60 else 'D'
        return jsonify({'score': score, 'grade': grade, 'checks': checks, 'passed': passed, 'total': len(checks), 'headers': h})
    except Exception as e:
        return jsonify({'error': str(e)}), 502

# ─── MODUL 2: SSL Certificate Inspector ───
def _tls_cert_info(hostname, port=443, timeout=4):
    """Fetch live cert via a TLS handshake. Fast (<1s) and independent
    of external APIs. Returns dict compatible with the crt.sh shape."""
    ctx = ssl.create_default_context()
    with socket.create_connection((hostname, port), timeout=timeout) as sock:
        with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
    # cert dates: 'Jun 25 19:48:39 2026 GMT'
    def _iso(s):
        try:
            return datetime.strptime(s, '%b %d %H:%M:%S %Y %Z').strftime('%Y-%m-%dT%H:%M:%S')
        except Exception:
            return s
    issuer = dict(x[0] for x in cert.get('issuer', []))
    subject = dict(x[0] for x in cert.get('subject', []))
    issuer_str = ', '.join(f'{k}={v}' for k, v in issuer.items())
    return {
        'issuer': issuer_str,
        'issuer_name': issuer_str,
        'common_name': subject.get('commonName', hostname),
        'not_before': _iso(cert.get('notBefore', '')),
        'not_after':  _iso(cert.get('notAfter', '')),
        'serial': (cert.get('serialNumber') or '')[:16],
        'total_certs': 1,
        'nvb': _iso(cert.get('notBefore', '')),
        'source': 'tls-handshake',
    }

@proxies_bp.route('/api/security/ssl')
def ssl_inspect():
    domain = 'bbmlab.duckdns.org'

    # Primary: direct TLS handshake — live, authoritative, <1s
    try:
        data = cached(f'ssl-tls:{domain}', 3600, lambda: _tls_cert_info(domain))
        return jsonify(data)
    except Exception as primary_err:
        # Fallback: crt.sh (CT logs) when TLS probe fails (DNS, firewall, etc.)
        try:
            logs = cached(f'ssl-crt:{domain}', 3600, lambda: safe_fetch(
                f'https://crt.sh/?q={domain}&output=json', timeout=15).json())
            if not logs:
                return jsonify({'error': 'no certs found', 'primary_error': str(primary_err)}), 404
            latest = sorted(logs, key=lambda x: x.get('not_after', ''), reverse=True)[0]
            return jsonify({
                'issuer': latest.get('issuer_name', 'Unknown'),
                'issuer_name': latest.get('issuer_name'),
                'common_name': latest.get('common_name', domain),
                'not_before': latest.get('not_before'),
                'not_after': latest.get('not_after'),
                'serial': (latest.get('serial_number') or '')[:16],
                'total_certs': len(logs),
                'nvb': latest.get('not_before'),
                'source': 'crt.sh',
            })
        except Exception as fallback_err:
            return jsonify({'error': f'tls: {primary_err} | crt.sh: {fallback_err}'}), 502

def _classify_severity(score):
    """Classify CVSS score per NVD v3.x standard.

    Overrides NVD's baseSeverity field, which is inconsistent for old
    CVSS v2-era CVEs (e.g. a 10.0 from 2014 can be reported as HIGH).
    """
    try:
        s = float(score)
    except (TypeError, ValueError):
        return 'NONE'
    if s >= 9.0:
        return 'CRITICAL'
    if s >= 7.0:
        return 'HIGH'
    if s >= 4.0:
        return 'MEDIUM'
    if s > 0:
        return 'LOW'
    return 'NONE'


def _parse_cve(item):
    cve = item.get('cve', {})
    metrics = cve.get('metrics', {})
    metric_list = (metrics.get('cvssMetricV31') or
                   metrics.get('cvssMetricV30') or
                   metrics.get('cvssMetricV2') or [])
    score = 0
    if metric_list:
        cvss_data = metric_list[0].get('cvssData', {})
        score = cvss_data.get('baseScore', 0)

    # Always classify from the numeric score — never trust NVD's
    # baseSeverity field (inconsistent for pre-v3.x records).
    severity = _classify_severity(score)

    descriptions = cve.get('descriptions', [])
    desc = next((d['value'] for d in descriptions if d.get('lang') == 'en'), '')

    return {
        'id': cve.get('id'),
        'score': round(score, 1),
        'severity': severity,
        'description': desc[:140],
        'published': cve.get('published', '')[:10],
        # Compatibility keys for frontend
        'cvss': round(score, 1),
        'sev': severity,
        'desc': desc[:140]
    }

# ─── MODUL 4: CVE Feed ───
@proxies_bp.route('/api/security/cves')
def cve_feed():
    keyword = request.args.get('q', 'docker')
    if keyword not in {'docker', 'nginx', 'flask', 'python', 'ubuntu'}:
        return jsonify({'error': 'keyword not allowed'}), 400
    try:
        data = cached(f'cve:{keyword}', 1800, lambda: safe_fetch(
            f'https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={keyword}&resultsPerPage=8',
            timeout=10).json())
        cves = [_parse_cve(item) for item in data.get('vulnerabilities', [])[:8]]
        return jsonify({'keyword': keyword, 'vulnerabilities': cves, 'total': len(cves)})
    except Exception as e:
        return jsonify({'error': str(e)}), 502
