from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from datetime import datetime

class servidor_1(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Servir el archivo HTML
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            with open('IP Capture.html', 'rb') as archivo_html:
                self.wfile.write(archivo_html.read())
        elif self.path == '/get-ip':
            # Obtener la IP del visitante
            ip_val = self.headers.get('X-Forwarded-For', self.client_address[0])
            
            # Si hay múltiples IPs en X-Forwarded-For (ej. "IP1, IP2"), tomar la primera
            if ',' in ip_val:
                ip_val = ip_val.split(',')[0].strip()
            
            # Guardar la IP en un archivo de texto
            self.guardar_ip(ip_val)
            
            # Enviar la respuesta en formato JSON
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'ip': ip_val}).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 - Página no encontrada')

    def guardar_ip(self, ip_val):
        # Obtener la fecha y hora actual
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Abrir el archivo en modo "append". Si no existe, se creará automáticamente.
        with open('IPv4.txt', 'a') as archivo_py:
            archivo_py.write(f"{fecha_hora} - {ip_val}\n")

if __name__ == "__main__":
    host = '0.0.0.0' # Escuchar en todas las interfaces
    puerto = 3000 # Puerto 3000
    servidor_val = HTTPServer((host, puerto), servidor_1)

    print(f"Servidor corriendo en http://{host}:{puerto}")

    try:
        servidor_val.serve_forever()
    except KeyboardInterrupt:
        pass
    
    servidor_val.server_close()