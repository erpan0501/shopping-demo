import unittest

from fastapi.testclient import TestClient

from app.main import app


class StaffConsoleTests(unittest.TestCase):
    def test_console_page_and_assets_are_served_with_safe_headers(self) -> None:
        with TestClient(app) as client:
            response = client.get("/internal/console")
            stylesheet = client.get("/internal/console/assets/staff-console.css")
            script = client.get("/internal/console/assets/staff-console.js")

        self.assertEqual(response.status_code, 200)
        self.assertIn("客服工作台", response.text)
        self.assertEqual(response.headers["cache-control"], "no-store")
        self.assertIn("frame-ancestors 'none'", response.headers["content-security-policy"])
        self.assertEqual(stylesheet.status_code, 200)
        self.assertEqual(script.status_code, 200)
        self.assertNotIn("STAFF_API_KEY", response.text)
