from http.server import BaseHTTPRequestHandler, HTTPServer


class AcceptEverything(BaseHTTPRequestHandler):
    def do_POST(self):
        self.rfile.read(int(self.headers.get("Content-Length", 0)))
        self.send_response(204)
        self.end_headers()


HTTPServer(("127.0.0.1", 3100), AcceptEverything).serve_forever()
