import http.server
import socketserver
import json

PORT = 8000

class SAMHandler(http.server.SimpleHTTPRequestHandler):

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", 'application/json')
        self.end_headers()

        self.data_string = self.rfile.read(int(self.headers['Content-Length']))

        data = json.loads(self.data_string)
        self.toggle_light(data["light"])

    def toggle_light(self, light_number):
        print(("Turning on light number {}".format(light_number)))


Handler = SAMHandler

httpd = socketserver.TCPServer(("", PORT), Handler)

print("serving at port {}".format(PORT))
httpd.serve_forever()