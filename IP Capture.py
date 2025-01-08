from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from datetime import datetime

class servidor_1(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Serve the HTML file
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open('IP Capture.html', 'rb') as archivo_html:
                self.wfile.write(archivo_html.read())
        elif self.path == '/get-ip':
            # Get the visitor's IP
            ip_val = self.headers.get('X-Forwarded-For', self.client_address[0])
            
            # If there are multiple IPs in X-Forwarded-For (e.g., "IP1, IP2"), take the first one
            if ',' in ip_val:
                ip_val = ip_val.split(',')[0].strip()
            
            # Save the IP to a text file
            self.guardar_ip(ip_val)
            
            # Send the response in JSON format
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'ip': ip_val}).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 - Page not found')

    def guardar_ip(self, ip_val):
        # Get the current date and time
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Open the file in "append" mode. If it doesn't exist, it will be created automatically.
        with open('IPv4.txt', 'a') as archivo_py:
            archivo_py.write(f"{fecha_hora} - {ip_val}\n")

if __name__ == "__main__":
    host = '0.0.0.0'  # Listen on all interfaces
    puerto = 3000     # Port 3000
    servidor_val = HTTPServer((host, puerto), servidor_1)

    print(f"Server running at http://{host}:{puerto}")

    try:
        servidor_val.serve_forever()
    except KeyboardInterrupt:
        pass
    
    servidor_val.server_close()