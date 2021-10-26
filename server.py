import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse
from urllib.parse import parse_qs
from httpobs.scanner.local import scan
import os
import logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


class ApiHandler(BaseHTTPRequestHandler):
    def _send_content(self, data, status=200, content_type="text/plain"):
        if isinstance(data, str):
            data = data.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)
        self.wfile.flush()

    def do_GET(self):
        url = parse.urlparse(self.path)
        queries = parse_qs(url.query)

        if url.path == "/domain":
            domain = queries.get("domain")
            if not domain:
                return self._send_content("", status=400)

            domain = domain[0]

            result = scan(domain)
            return self._send_content(json.dumps(result), 200, "application/json")

        return self._send_content("", status=404)




def run(server_class=HTTPServer, handler_class=ApiHandler):
    server_address = ('0.0.0.0', os.environ.get("API_PORT", 9000))
    httpd = server_class(server_address, handler_class)
    logger.info("Server started")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
