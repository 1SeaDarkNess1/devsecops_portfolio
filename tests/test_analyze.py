import sys
import unittest
from unittest.mock import MagicMock

# Mock out psutil and platform before importing app
sys.modules['psutil'] = MagicMock()
sys.modules['platform'] = MagicMock()

import app.app as application

class TestAnalyzePayload(unittest.TestCase):
    def setUp(self):
        self.app = application.app.test_client()
        self.app.testing = True

    def test_safe_payload(self):
        response = self.app.post('/api/analyze', json={"payload": "hello world"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["level"], "SAFE")
        self.assertEqual(data["type"], "None")
        self.assertEqual(data["original_payload"], "hello world")

    def test_missing_payload(self):
        response = self.app.post('/api/analyze', json={})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["level"], "SAFE")
        self.assertEqual(data["type"], "None")
        self.assertEqual(data["original_payload"], "")

    def test_sql_injection_union(self):
        response = self.app.post('/api/analyze', json={"payload": "UNION SELECT * FROM users"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["level"], "CRITICAL")
        self.assertEqual(data["type"], "SQL Injection (OWASP A03:2021)")

    def test_sql_injection_or(self):
        response = self.app.post('/api/analyze', json={"payload": "admin' or 1=1 --"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["level"], "CRITICAL")
        self.assertEqual(data["type"], "SQL Injection (OWASP A03:2021)")

    def test_xss_script(self):
        response = self.app.post('/api/analyze', json={"payload": "<script>alert(1)</script>"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["level"], "CRITICAL")
        self.assertEqual(data["type"], "Cross-Site Scripting (OWASP A03:2021)")

    def test_xss_onerror(self):
        response = self.app.post('/api/analyze', json={"payload": "<img src=x onerror=alert(1)>"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["level"], "CRITICAL")
        self.assertEqual(data["type"], "Cross-Site Scripting (OWASP A03:2021)")

    def test_path_traversal_dotdot(self):
        response = self.app.post('/api/analyze', json={"payload": "../../../etc/passwd"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["level"], "CRITICAL")
        self.assertEqual(data["type"], "Path Traversal (OWASP A01:2021)")

    def test_path_traversal_etc_passwd(self):
        response = self.app.post('/api/analyze', json={"payload": "/etc/passwd"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["level"], "CRITICAL")
        self.assertEqual(data["type"], "Path Traversal (OWASP A01:2021)")

    def test_exception_handling(self):
        # Trigger an exception by sending invalid JSON string instead of an object
        response = self.app.post('/api/analyze', data="Invalid JSON", content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data["status"], "error")

if __name__ == '__main__':
    unittest.main()
