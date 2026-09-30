"""Local archive browser. Bind to localhost only."""

from __future__ import annotations

import json
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

import catalog

STATIC = Path(__file__).resolve().parent / "static"
HOST = "127.0.0.1"
PORT = 8765


def _json_bytes(payload: dict, status: int = 200) -> tuple[int, bytes]:
    return status, json.dumps(payload).encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args) -> None:
        return

    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        data = json.loads(raw.decode("utf-8"))
        if not isinstance(data, dict):
            raise ValueError("expected an object")
        return data

    def _api(self, method: str, parts: list[str]) -> tuple[int, bytes]:
        try:
            if method == "GET" and parts == ["catalog"]:
                return _json_bytes(catalog.catalog())
            if method == "GET" and len(parts) == 2 and parts[0] == "items":
                return _json_bytes(catalog.load_item(parts[1]))
            if method == "PUT" and len(parts) == 2 and parts[0] == "items":
                return _json_bytes(catalog.save_item(parts[1], self._read_json()))
            if method == "POST" and parts == ["items"]:
                return _json_bytes(catalog.create_item(self._read_json()), 201)
            if method == "POST" and len(parts) == 4 and parts[0] == "items" and parts[2] == "restore":
                return _json_bytes(catalog.restore_item(parts[1], parts[3]))
            return _json_bytes({"error": "not found"}, 404)
        except FileNotFoundError:
            return _json_bytes({"error": "not found"}, 404)
        except ValueError as exc:
            return _json_bytes({"error": str(exc)}, 400)
        except json.JSONDecodeError:
            return _json_bytes({"error": "invalid JSON"}, 400)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/"):
            status, body = self._api("GET", [part for part in parsed.path[5:].split("/") if part])
            self._send(status, body, "application/json")
            return
        path = parsed.path
        if path in ("", "/"):
            path = "/index.html"
        file_path = (STATIC / path.lstrip("/")).resolve()
        if not str(file_path).startswith(str(STATIC.resolve())) or not file_path.is_file():
            self._send(404, b"not found", "text/plain; charset=utf-8")
            return
        mime = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        self._send(200, file_path.read_bytes(), mime)

    def do_PUT(self) -> None:
        parsed = urlparse(self.path)
        if not parsed.path.startswith("/api/"):
            self._send(404, b"not found", "text/plain; charset=utf-8")
            return
        status, body = self._api("PUT", [part for part in parsed.path[5:].split("/") if part])
        self._send(status, body, "application/json")

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if not parsed.path.startswith("/api/"):
            self._send(404, b"not found", "text/plain; charset=utf-8")
            return
        status, body = self._api("POST", [part for part in parsed.path[5:].split("/") if part])
        self._send(status, body, "application/json")


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Directive archive at http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
