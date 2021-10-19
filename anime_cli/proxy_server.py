"""
Sets up a proxy server, which automatically adds required header
to each request. It makes it possible to run videos in players
where passing in http-header is not supported
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler

import requests


def proxyServer(headers, serverAddress) -> HTTPServer:
    """returns the http server

    Args:
        headers: The headers to send along with the request
        serverAddress: The server address to use for the server

    Returns:
        HTTPServer object
    """

    class ProxyHTTPRequestHandler(SimpleHTTPRequestHandler):
        """A proxy http request handler
        The request to the server is handled through it

        Example:
            On a request to /http://example.com, the server will
            first get the content of http://example.com by sending
            required headers with the request, then
            send the same content to the user
        """

        protocol_version = "HTTP/1.0"

        def do_GET(self, body=True):
            """The function which handles the get request to the server"""
            # Get the url
            hostname = self.path[1:]
            # Get the content from the url, along with the headers
            resp = requests.get(hostname, headers=headers)

            # Send respose status to be same as response status from above request
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

            # Send the content from the request to the user as it is
            self.wfile.write(resp.content)
            return

        # Disable logging for requests
        def log_request(self, code=..., size=...) -> None:
            pass

    return HTTPServer(serverAddress, ProxyHTTPRequestHandler)
