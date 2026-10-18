"""Exercise disabled settings, actual API responses, and the total deadline."""
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from network_check import NetworkAccessError, require_network


@contextmanager
def endpoint(mode="ok"):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_GET(self):
            if mode == "stall":
                time.sleep(11)
                return
            if self.path == "/version":
                payload = {"api_version": "v1", "host_description": "ProPresenter test"}
                if mode == "wrong_app":
                    payload = {"name": "Another app"}
            elif self.path == "/v1/libraries":
                if mode == "denied":
                    self.send_error(403)
                    return
                payload = []
            else:
                self.send_error(404)
                return
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(payload).encode())

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()


class PreflightTests(unittest.TestCase):
    def test_network_off_stops_without_starting_probe(self):
        with tempfile.TemporaryDirectory() as temp:
            prefs = Path(temp) / "RenewedVision/ProPresenter/Preferences/NetworkPreferences.proPref"
            prefs.parent.mkdir(parents=True)
            prefs.write_text("EnableNetwork=false;\nNetworkPort=54908;\n")
            with patch.dict(os.environ, {"APPDATA": temp, "PROPRESENTER_API_URL": ""}), patch("network_check.subprocess.run") as run:
                with self.assertRaisesRegex(NetworkAccessError, "turned off"):
                    require_network()
                run.assert_not_called()

    def test_reachable_api(self):
        with endpoint() as url:
            self.assertEqual(require_network(url)["libraries"], 0)

    def test_wrong_app_rejected(self):
        with endpoint("wrong_app") as url:
            with self.assertRaisesRegex(NetworkAccessError, "not a supported"):
                require_network(url)

    def test_library_access_required(self):
        with endpoint("denied") as url:
            with self.assertRaisesRegex(NetworkAccessError, "403"):
                require_network(url)

    def test_stalled_api_exits_within_ten_seconds(self):
        with endpoint("stall") as url:
            start = time.monotonic()
            with self.assertRaises(NetworkAccessError):
                require_network(url)
            self.assertLess(time.monotonic() - start, 10)

    def test_permission_error_is_not_misreported_as_network_off(self):
        result = subprocess.CompletedProcess([], 2, "", "[WinError 10013] forbidden by its access permissions")
        with patch("network_check.subprocess.run", return_value=result):
            with self.assertRaisesRegex(NetworkAccessError, "OS or sandbox"):
                require_network("http://127.0.0.1:1234")

    def test_setup_exits_nonzero_on_failure(self):
        with endpoint("wrong_app") as url:
            result = subprocess.run([sys.executable, str(Path(__file__).resolve().parents[1] / "check_setup.py"), "--api-url", url], capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 2)
            self.assertIn("Setup stopped", result.stderr)


if __name__ == "__main__":
    unittest.main()
