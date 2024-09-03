import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from ai import get_ai_response  

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        sentence = "What is the capital of France?"
        language = 'korean'
  
        response = get_ai_response(sentence, language)
        response_json = json.dumps(response)
      
        self.send_response(200)
        self.send_header('Content-type', 'application/json;')
        self.end_headers()

        self.wfile.write(response_json.encode())
        return

def run(server_class=HTTPServer, handler_class=Handler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()