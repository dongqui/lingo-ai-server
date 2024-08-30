from http.server import BaseHTTPRequestHandler
import ai

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        question = "What is the capital of France?"
        response = ai.get_response(question)

        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write('Hello, world!'.encode('utf-8'))
        return

