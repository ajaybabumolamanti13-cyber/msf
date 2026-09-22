import unittest
from fastapi.testclient import TestClient
from MFIS.backend.main import app

client = TestClient(app)


class MFISTestCase(unittest.TestCase):
    def test_root(self):
        response = client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_cases_endpoint(self):
        response = client.get('/api/cases/')
        self.assertEqual(response.status_code, 200)

    def test_devices_endpoint(self):
        response = client.get('/api/devices/scan')
        self.assertEqual(response.status_code, 200)

    def test_artifacts_summary(self):
        response = client.get('/api/artifacts/summary')
        self.assertEqual(response.status_code, 200)

    def test_analysis_route(self):
        response = client.post('/api/analysis/run')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
