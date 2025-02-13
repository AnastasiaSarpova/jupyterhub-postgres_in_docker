from http.server import BaseHTTPRequestHandler, HTTPServer
import os

METRICS_FILE = "/tmp/notebook_metrics_jupyter.prom"

class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if os.path.exists(METRICS_FILE):
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            with open(METRICS_FILE, "r") as f:
                self.wfile.write(f.read().encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Metrics file not found")

def run(server_class=HTTPServer, handler_class=MetricsHandler, port=17666):
    server_address = ("0.0.0.0", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting HTTP server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()