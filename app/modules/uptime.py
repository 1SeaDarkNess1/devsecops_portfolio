"""
UptimeRobot proxy endpoint.

Reads the UptimeRobot read-only API key from the UPTIMEROBOT_API_KEY
environment variable (never commit the key). Returns the 1/7/30-day
uptime ratios for the first configured monitor so the frontend can
render real uptime instead of a hardcoded 99.9%.

Response shape:
    {
      "ok": true,
      "monitor": "bbmlab.duckdns.org",
      "status": 2,            # 2 = up, 8 = seems down, 9 = down
      "ratios": {"1d": 99.91, "7d": 99.87, "30d": 99.93},
      "updated": 1712847321
    }

Failure cases return 2xx with {"ok": false, "error": "..."} so the
frontend can gracefully fall back to a "--" placeholder without a
console error.
"""
import os
from time import time

import requests
from flask import Blueprint, jsonify

from ..extensions import limiter

uptime_bp = Blueprint('uptime', __name__)

UR_ENDPOINT = 'https://api.uptimerobot.com/v2/getMonitors'
UR_TIMEOUT = 8

# Short in-memory cache so a page refresh storm doesn't burn the
# UptimeRobot API budget (free tier = 10 req/min).
_cache = {'ts': 0, 'data': None}
_CACHE_TTL = 120  # seconds


@uptime_bp.route('/api/uptime')
@limiter.exempt
def uptime():
    now = time()
    if _cache['data'] and (now - _cache['ts']) < _CACHE_TTL:
        return jsonify(_cache['data'])

    api_key = os.environ.get('UPTIMEROBOT_API_KEY', '').strip()
    if not api_key:
        return jsonify({
            'ok': False,
            'error': 'UPTIMEROBOT_API_KEY not configured',
            'updated': int(now),
        })

    try:
        r = requests.post(
            UR_ENDPOINT,
            data={
                'api_key': api_key,
                'format': 'json',
                'custom_uptime_ratios': '1-7-30',
                'logs': 0,
            },
            headers={
                'Cache-Control': 'no-cache',
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            timeout=UR_TIMEOUT,
        )
    except requests.exceptions.Timeout:
        return jsonify({'ok': False, 'error': 'UptimeRobot timeout', 'updated': int(now)})
    except requests.exceptions.RequestException as e:
        return jsonify({'ok': False, 'error': f'UptimeRobot request failed: {str(e)[:160]}', 'updated': int(now)})

    if r.status_code != 200:
        return jsonify({
            'ok': False,
            'error': f'UptimeRobot HTTP {r.status_code}',
            'updated': int(now),
        })

    try:
        payload = r.json()
    except ValueError:
        return jsonify({'ok': False, 'error': 'UptimeRobot returned non-JSON', 'updated': int(now)})

    if payload.get('stat') != 'ok':
        detail = (payload.get('error') or {}).get('message', 'unknown error')
        return jsonify({'ok': False, 'error': f'UptimeRobot: {detail}', 'updated': int(now)})

    monitors = payload.get('monitors') or []
    if not monitors:
        return jsonify({'ok': False, 'error': 'No monitors configured', 'updated': int(now)})

    m = monitors[0]
    ratios_str = (m.get('custom_uptime_ratio') or '').split('-')
    def _pct(i):
        try:
            return round(float(ratios_str[i]), 2)
        except (IndexError, ValueError, TypeError):
            return None

    data = {
        'ok': True,
        'monitor': m.get('friendly_name') or m.get('url') or 'unknown',
        'url': m.get('url'),
        'status': m.get('status'),  # 2=up, 8=seems down, 9=down, 0=paused
        'ratios': {
            '1d': _pct(0),
            '7d': _pct(1),
            '30d': _pct(2),
        },
        'updated': int(now),
    }

    _cache['ts'] = now
    _cache['data'] = data
    return jsonify(data)
