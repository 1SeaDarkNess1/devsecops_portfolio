import os
import requests
from flask import Blueprint, jsonify
from time import time
from datetime import datetime

github_bp = Blueprint('github', __name__)
REPO = os.environ.get('GITHUB_REPO', '1SeaDarkNess1/devsecops_portfolio')
TOKEN = os.environ.get('GITHUB_TOKEN', '')
_cache = {'ts': 0, 'data': None}

def _duration_seconds(started, updated):
    if not started or not updated:
        return None
    try:
        s = datetime.fromisoformat(started.replace('Z', '+00:00'))
        u = datetime.fromisoformat(updated.replace('Z', '+00:00'))
        return int((u - s).total_seconds())
    except (ValueError, AttributeError):
        return None

@github_bp.route('/api/github/runs')
def github_runs():
    if time() - _cache['ts'] < 60 and _cache['data']:
        return jsonify(_cache['data'])

    headers = {
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'User-Agent': 'BBM-Lab/1.0',
    }
    if TOKEN:
        headers['Authorization'] = f'Bearer {TOKEN}'

    try:
        r = requests.get(
            f'https://api.github.com/repos/{REPO}/actions/runs',
            params={'per_page': 8},
            headers=headers,
            timeout=10
        )
        if r.status_code != 200:
            detail = 'unknown'
            try:
                detail = r.json().get('message', r.text[:200])
            except Exception:
                detail = r.text[:200]
            return jsonify({'error': f'GitHub API {r.status_code}', 'detail': detail, 'runs': []}), 502

        payload = r.json()
        runs = []
        for run in payload.get('workflow_runs', [])[:8]:
            head_commit = run.get('head_commit') or {}
            actor = run.get('actor') or {}
            started = run.get('run_started_at')
            updated = run.get('updated_at')
            runs.append({
                'id': run.get('id'),
                'name': run.get('name', 'workflow'),
                'status': run.get('status'),
                'conclusion': run.get('conclusion'),
                'sha': (run.get('head_sha') or '')[:7],
                'message': (head_commit.get('message') or '').split('\n')[0][:80],
                'actor': actor.get('login', 'unknown'),
                'started': started,
                'updated': updated,
                'duration_s': _duration_seconds(started, updated) if run.get('status') == 'completed' else None,
                'url': run.get('html_url'),
                'event': run.get('event'),
            })

        data = {
            'runs': runs,
            'repo': REPO,
            'total_count': payload.get('total_count', 0),
            'fetched_at': int(time()),
            'rate_limit_remaining': r.headers.get('x-ratelimit-remaining', 'unknown'),
        }
        _cache['ts'] = time()
        _cache['data'] = data
        return jsonify(data)

    except requests.exceptions.Timeout:
        return jsonify({'error': 'GitHub API timeout', 'runs': []}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'request failed', 'detail': str(e)[:200], 'runs': []}), 502
    except Exception as e:
        return jsonify({'error': 'internal', 'detail': str(e)[:200], 'runs': []}), 500
