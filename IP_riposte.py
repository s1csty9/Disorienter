import random
import socket
import struct
from mitmproxy import http, ctx, master
import requests

def get_public_ip():
    response = requests.get("https://api.ipify.org?format=json")
    if response.status_code == 200:
        data = response.json()
        return data["ip"]
    else:
        return None

public_ip = get_public_ip()

class RequestInterceptor:
    def __init__(self):
        self.random_ip = None

    def request(self, flow: http.HTTPFlow) -> None:
        if "discord.com/api/webhooks" in flow.request.pretty_host:
            if public_ip and public_ip in flow.request.text:
                self.random_ip = self.generate_random_ip()
                modified_body = flow.request.text.replace(public_ip, self.random_ip)
                flow.request.text = modified_body

    def response(self, flow: http.HTTPFlow) -> None:
        if self.random_ip and self.random_ip in flow.response.text:
            modified_body = flow.response.text.replace(self.random_ip, public_ip)
            flow.response.text = modified_body

    def generate_random_ip(self):
        return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

addons = [
    RequestInterceptor()
]

def start():
    config = ctx.default_config
    config.options.update(
        ssl_insecure=True
    )
    m = master.Master(options=config)
    m.addons.add(addons)
    m.run()

if __name__ == "__main__":
    start()
