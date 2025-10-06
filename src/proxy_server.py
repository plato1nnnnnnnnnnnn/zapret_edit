import socketserver
from http.server import BaseHTTPRequestHandler
import json
import requests

with open('src/config.json', 'r') as f:
    config = json.load(f)
ENABLED_SERVICES = config.get('enabled_services', [])
EXTERNAL_PROXY = config.get('external_proxy', None)

SERVICE_DOMAINS = {
    'discord': ['discord.com', 'cdn.discordapp.com'],
    'youtube': ['youtube.com', 'youtu.be', 'googlevideo.com'],
    'soundcloud': ['soundcloud.com'],
    'spotify': ['spotify.com', 'audio-ak.spotify.com'],
    'telegram': ['t.me', 'telegram.org'],
    'whatsapp': ['whatsapp.com'],
    'instagram': ['instagram.com'],
    'facebook': ['facebook.com'],
    'twitter': ['twitter.com'],
    'tiktok': ['tiktok.com'],
    'snapchat': ['snapchat.com'],
    'linkedin': ['linkedin.com'],
    'pinterest': ['pinterest.com'],
    'reddit': ['reddit.com'],
    'vimeo': ['vimeo.com'],
    'tumblr': ['tumblr.com']
}

def detect_service_by_host(host):
    for service, domains in SERVICE_DOMAINS.items():
        if any(host.endswith(d) for d in domains):
            return service
    return None


import socket

class ProxyHandler(BaseHTTPRequestHandler):
    def do_CONNECT(self):
        host, port = self.path.split(":")
        service = detect_service_by_host(host)
        if service and service in ENABLED_SERVICES and EXTERNAL_PROXY:
            # Перенаправление через внешний прокси (CONNECT)
            try:
                proxy_host, proxy_port = EXTERNAL_PROXY.replace("http://","").split(":")
                proxy_port = int(proxy_port)
                with socket.create_connection((proxy_host, proxy_port)) as proxy_sock:
                    connect_str = f"CONNECT {self.path} HTTP/1.1\r\nHost: {self.path}\r\n\r\n"
                    proxy_sock.sendall(connect_str.encode())
                    response = proxy_sock.recv(4096)
                    self.wfile.write(response)
                    if b"200 Connection established" in response:
                        self.connection.setblocking(0)
                        proxy_sock.setblocking(0)
                        try:
                            while True:
                                data = self.connection.recv(4096)
                                if data:
                                    proxy_sock.sendall(data)
                                data = proxy_sock.recv(4096)
                                if data:
                                    self.connection.sendall(data)
                        except Exception:
                            pass
            except Exception as e:
                self.send_error(502, f"Proxy CONNECT error: {e}")
        else:
            # Прямое соединение
            try:
                with socket.create_connection((host, int(port))) as remote_sock:
                    self.send_response(200, "Connection established")
                    self.end_headers()
                    self.connection.setblocking(0)
                    remote_sock.setblocking(0)
                    try:
                        while True:
                            data = self.connection.recv(4096)
                            if data:
                                remote_sock.sendall(data)
                            data = remote_sock.recv(4096)
                            if data:
                                self.connection.sendall(data)
                    except Exception:
                        pass
            except Exception as e:
                self.send_error(502, f"Direct CONNECT error: {e}")

    def do_GET(self):
        host = self.headers.get('Host', '')
        service = detect_service_by_host(host)
        url = f"http://{host}{self.path}"
        if service and service in ENABLED_SERVICES and EXTERNAL_PROXY:
            # Перенаправление через внешний прокси
            proxies = {
                'http': EXTERNAL_PROXY,
                'https': EXTERNAL_PROXY
            }
            try:
                resp = requests.get(url, headers=self.headers, proxies=proxies, timeout=10)
                self.send_response(resp.status_code)
                for k, v in resp.headers.items():
                    self.send_header(k, v)
                self.end_headers()
                self.wfile.write(resp.content)
            except Exception as e:
                self.send_error(502, f"Proxy error: {e}")
        else:
            # Пропускать остальной трафик напрямую
            try:
                resp = requests.get(url, headers=self.headers, timeout=10)
                self.send_response(resp.status_code)
                for k, v in resp.headers.items():
                    self.send_header(k, v)
                self.end_headers()
                self.wfile.write(resp.content)
            except Exception as e:
                self.send_error(502, f"Direct error: {e}")

if __name__ == "__main__":
    PORT = 8080
    with socketserver.ThreadingTCPServer(("", PORT), ProxyHandler) as httpd:
        print(f"Proxy server running on port {PORT}")
        httpd.serve_forever()
