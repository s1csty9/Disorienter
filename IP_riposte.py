import random
import socket
import struct
from mitmproxy import http, ctx
import requests

def get_public_ip():
    response = requests.get("https://api.ipify.org?format=json")
    if response.status_code == 200:
        data = response.json()
        return data["ip"]
    else:
        return None

public_ip = get_public_ip()
while 1 == 1:
  class RequestInterceptor:
      def request(self, flow: http.HTTPFlow) -> None:
          if "discord.com/api/webhooks" in flow.request.pretty_host:
              if public_ip and public_ip in flow.request.text:
                  random_ip = self.generate_random_ip()
                  modified_body = flow.request.text.replace(public_ip, random_ip)
                  flow.request.text = modified_body

      def generate_random_ip(self):
          return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

  addons = [
      RequestInterceptor()
  ]
