from http.server import HTTPServer, BaseHTTPRequestHandler
import json

HOST = '192.168.0.38'
port = 9999

queue = []

def append_on_queue(command):
    global queue
    queue.append(command)

def dequeue():
    global queue
    queue.pop(0)

class NeuralHTTP(BaseHTTPRequestHandler):
    def do_GET(self):
        global queue
        q = ','.join(queue)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(bytes(q,"utf-8"))

server = HTTPServer((HOST,port), NeuralHTTP)

print("Server is now running...")

server.serve_forever()
server.server_close()