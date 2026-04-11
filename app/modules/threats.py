from flask import Blueprint, jsonify
import json, os
from time import time

threats_bp = Blueprint('threats', __name__)
THREATS_PATH = os.path.join(os.path.dirname(__file__), '..', 'static', 'threats.json')

@threats_bp.route('/api/threats')
def threats_data():
    try:
        if not os.path.exists(THREATS_PATH):
            return jsonify({'attacks': [], 'total': 0, 'updated': int(time())})
            
        with open(THREATS_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({'attacks': [], 'total': 0, 'updated': int(time()), 'error': str(e)})
