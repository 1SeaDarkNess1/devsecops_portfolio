from flask import Blueprint, jsonify
import json, os

sbom_bp = Blueprint('sbom', __name__)

# Paths relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SBOM_PATH = os.path.join(BASE_DIR, '..', 'static', 'sbom.json')
TRIVY_PATH = os.path.join(BASE_DIR, '..', 'static', 'trivy.json')

@sbom_bp.route('/api/sbom')
def sbom_summary():
    try:
        if not os.path.exists(SBOM_PATH):
            return jsonify({'error': 'SBOM file not found', 'path': SBOM_PATH}), 404
            
        with open(SBOM_PATH, 'r', encoding='utf-8') as f:
            sbom = json.load(f)
            
        # Syft uses 'artifacts', generic CycloneDX uses 'components'
        artifacts = sbom.get('artifacts') or sbom.get('components') or []
        
        processed = []
        for a in artifacts[:200]:
            # Handle Syft license (list of strings) or CycloneDX (list of objects)
            lics = a.get('licenses') or []
            if lics and isinstance(lics[0], str):
                lic_str = lics[0]
            elif lics and isinstance(lics[0], dict):
                lic_str = lics[0].get('license', {}).get('id') or lics[0].get('name') or 'unknown'
            else:
                lic_str = 'unknown'
                
            processed.append({
                'name': a.get('name'),
                'version': a.get('version'),
                'type': a.get('type'),
                'license': lic_str,
            })
            
        return jsonify({
            'total': len(artifacts),
            'components': processed,
            'generated': sbom.get('metadata', {}).get('timestamp') or 'recently'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sbom_bp.route('/api/trivy')
def trivy_results():
    try:
        if not os.path.exists(TRIVY_PATH):
            return jsonify({'error': 'Trivy report not found'}), 404
            
        with open(TRIVY_PATH, 'r', encoding='utf-8') as f:
            trivy = json.load(f)
            
        vulns = []
        for result in trivy.get('Results', []):
            for v in result.get('Vulnerabilities', []) or []:
                vulns.append({
                    'id': v.get('VulnerabilityID'),
                    'pkg': v.get('PkgName'),
                    'version': v.get('InstalledVersion'),
                    'fixed': v.get('FixedVersion', '—'),
                    'severity': v.get('Severity'),
                    'title': (v.get('Title', '') or v.get('Description', ''))[:100],
                })
                
        counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0, 'UNKNOWN': 0}
        for v in vulns:
            s = v['severity'].upper()
            if s in counts:
                counts[s] += 1
            else:
                counts['UNKNOWN'] += 1
                
        return jsonify({
            'total': len(vulns),
            'counts': counts,
            'vulnerabilities': vulns[:50] # Top 50
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
