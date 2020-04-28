from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from gh_actions_client import get_gh_actions_client


PORT = 8080

class KubeMlOpsBotRequestHandler(BaseHTTPRequestHandler):
        
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        print(body.decode())
        payload = json.loads(body)
        get_gh_actions_client().send_dispatch_event(payload['event_type'], payload)        
        self.send_response(200)
        self.end_headers()
    
httpd = HTTPServer(('', PORT), KubeMlOpsBotRequestHandler)
httpd.serve_forever()