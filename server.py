import json, os, sqlite3
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(ROOT, 'prompt-master.db')
DIST = os.path.join(ROOT, 'dist')

def init_db():
    con = sqlite3.connect(DB)
    con.execute('CREATE TABLE IF NOT EXISTS app_state (id INTEGER PRIMARY KEY CHECK(id=1), data TEXT NOT NULL, updated_at TEXT DEFAULT CURRENT_TIMESTAMP)')
    con.commit(); con.close()

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs): super().__init__(*args, directory=DIST, **kwargs)
    def do_GET(self):
        if urlparse(self.path).path == '/api/data':
            con=sqlite3.connect(DB); row=con.execute('SELECT data FROM app_state WHERE id=1').fetchone(); con.close()
            self.send_response(200); self.send_header('Content-Type','application/json'); self.end_headers(); self.wfile.write((row[0] if row else '{}').encode()); return
        return super().do_GET()
    def do_POST(self):
        if urlparse(self.path).path != '/api/data': self.send_error(404); return
        size=int(self.headers.get('Content-Length','0')); data=self.rfile.read(size).decode()
        json.loads(data)
        con=sqlite3.connect(DB); con.execute('INSERT INTO app_state(id,data) VALUES(1,?) ON CONFLICT(id) DO UPDATE SET data=excluded.data,updated_at=CURRENT_TIMESTAMP',(data,)); con.commit(); con.close()
        self.send_response(204); self.end_headers()
    def log_message(self, fmt, *args): pass

if __name__ == '__main__':
    init_db(); print('Prompt Master aberto em http://127.0.0.1:8765')
    ThreadingHTTPServer(('127.0.0.1',8765),Handler).serve_forever()
