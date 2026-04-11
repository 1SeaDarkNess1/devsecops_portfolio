from flask import Blueprint, jsonify, request
import requests, socket, ipaddress
from urllib.parse import urlparse
from time import time
from extensions import limiter

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
@proxies_bp.route('/api/security/ssl')
def ssl_inspect():
    domain = 'bbmlab.duckdns.org'
    try:
        data = cached(f'ssl:{domain}', 3600, lambda: safe_fetch(
            f'https://crt.sh/?q={domain}&output=json').json())
        if not data:
            return jsonify({'error': 'no certs found'}), 404
        # Sort by latest
        latest = sorted(data, key=lambda x: x.get('not_after', ''), reverse=True)[0]
        return jsonify({
            'issuer': latest.get('issuer_name', 'Unknown'),
            'common_name': latest.get('common_name', domain),
            'not_before': latest.get('not_before'),
            'not_after': latest.get('not_after'),
            'serial': latest.get('serial_number', '')[:16],
            'total_certs': len(data),
            'nvb': latest.get('not_before'), # compatibility for frontend
            'issuer_name': latest.get('issuer_name') # compatibility
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 502

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
        cves = []
        for item in data.get('vulnerabilities', [])[:8]:
            cve_data = item['cve']
            metric = (cve_data.get('metrics', {}).get('cvssMetricV31') or
                      cve_data.get('metrics', {}).get('cvssMetricV30') or [{}])[0]
            score = metric.get('cvssData', {}).get('baseScore', 0)
            cves.append({
                'id': cve_data['id'],
                'score': score,
                'cvss': score, # compatibility
                'severity': 'CRITICAL' if score >= 9 else 'HIGH' if score >= 7 else 'MEDIUM' if score >= 4 else 'LOW',
                'sev': 'CRITICAL' if score >= 9 else 'HIGH' if score >= 7 else 'MEDIUM' if score >= 4 else 'LOW', # compatibility
                'description': (cve_data.get('descriptions', [{}])[0].get('value', ''))[:140],
                'desc': (cve_data.get('descriptions', [{}])[0].get('value', ''))[:140], # compatibility
                'published': cve_data.get('published', '')[:10],
            })
        return jsonify({'keyword': keyword, 'vulnerabilities': cves, 'total': len(cves)})
    except Exception as e:
        return jsonify({'error': str(e)}), 502
