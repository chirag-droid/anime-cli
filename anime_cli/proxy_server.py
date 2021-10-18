"""
Sets up a proxy server, which automatically adds required header
to each request. It makes it possible to run videos in players
where passing in http-header is not supported
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler

import requests


def proxyServer(headers, serverAddress) -> HTTPServer:
    class ProxyHTTPRequestHandler(SimpleHTTPRequestHandler):
        protocol_version = "HTTP/1.0"

        def do_GET(self, body=True):
            # Parse request
            hostname = self.path[1:]

            resp = requests.get(hostname, headers=headers)

            self.send_response(resp.status_code)

            exclude_headers = [
                "content-encoding",
                "content-length",
                "transfer-encoding",
                "connection",
            ]
            for k in resp.headers.keys():
                if k.lower() in exclude_headers:
                    continue
                self.send_header(k, resp.headers.get(k))
            self.end_headers()

            self.wfile.write(resp.content)
            return

    return HTTPServer(serverAddress, ProxyHTTPRequestHandler)
