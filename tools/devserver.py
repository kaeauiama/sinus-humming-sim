"""Static file server for the project root that also accepts POST /save?name=<dir>/<file> into results/lbm/.

Used by the precompute page (pages/agefield.template.html) to store scalar-field snapshots without downloads.
Binds 127.0.0.1 only. Run: python tools/devserver.py  (port 8767; see .claude/launch.json "dev")
"""
import http.server, os, re, json
from urllib.parse import urlparse, parse_qs

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'results', 'lbm')
SAFE = re.compile(r'^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$')

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=ROOT, **k)
    def do_POST(self):
        u = urlparse(self.path)
        name = parse_qs(u.query).get('name', [''])[0]
        if u.path != '/save' or not SAFE.match(name) or '..' in name:
            self.send_error(400, 'bad name'); return
        n = int(self.headers.get('Content-Length', 0))
        if n > 64 * 1024 * 1024: self.send_error(413); return
        data = self.rfile.read(n)
        path = os.path.join(OUT, *name.split('/'))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f: f.write(data)
        body = json.dumps({'saved': name, 'bytes': len(data)}).encode()
        self.send_response(200); self.send_header('Content-Type', 'application/json'); self.send_header('Content-Length', str(len(body)))
        self.end_headers(); self.wfile.write(body)
    def log_message(self, fmt, *args):
        if self.command == 'POST': super().log_message(fmt, *args)

if __name__ == '__main__':
    http.server.ThreadingHTTPServer(('127.0.0.1', 8767), H).serve_forever()
