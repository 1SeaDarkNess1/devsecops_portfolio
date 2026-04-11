from flask import Blueprint, jsonify
import requests, os
from time import time

github_bp = Blueprint('github', __name__)
REPO = '1SeaDarkNess1/devsecops_portfolio'
_cache = {'ts': 0, 'data': None}

@github_bp.route('/api/github/runs')
def github_runs():
    if time() - _cache['ts'] < 60 and _cache['data']:
        return jsonify(_cache['data'])
    
    token = os.getenv('GITHUB_TOKEN')
    headers = {'Accept': 'application/vnd.github+json'}
    if token:
        headers['Authorization'] = f'token {token}'
        
    try:
        r = requests.get(f'https://api.github.com/repos/{REPO}/actions/runs?per_page=8',
                         timeout=8, headers=headers)
        r.raise_for_status()
        runs = []
        for run in r.json().get('workflow_runs', []):
            runs.append({
                'id': run['id'],
                'name': run['name'],
                'status': run['status'],
                'conclusion': run['conclusion'],
                'sha': run['head_sha'][:7],
                'message': run['head_commit']['message'].split('\n')[0][:80],
                'actor': run['actor']['login'],
                'started': run['run_started_at'],
                'duration_s': int((requests.utils.parsedate_to_datetime(run['updated_at']) -
                                   requests.utils.parsedate_to_datetime(run['run_started_at'])).total_seconds())
                              if run['status'] == 'completed' else None,
                'url': run['html_url'],
            })
        data = {'runs': runs, 'repo': REPO, 'fetched': int(time())}
        _cache['ts'] = time()
        _cache['data'] = data
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 502
