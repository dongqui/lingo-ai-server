import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from ai import get_ai_response  

class Handler(BaseHTTPRequestHandler):

    def do_POST(self):
        # 요청 크기 가져오기
        content_length = int(self.headers['Content-Length'])
        
        # 요청 본문에서 데이터 읽기
        post_data = self.rfile.read(content_length)
        
        # JSON 형식의 데이터를 파싱
        data = json.loads(post_data)
        sentence = data.get('sentence')
        language = data.get('language')
  
        response = get_ai_response(sentence, language)
        response_json = json.dumps(response)
      
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
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