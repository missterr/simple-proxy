#!/usr/bin/env python

import argparse
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

import requests

from parser import Parser
from settings import HOST


class ProxyHTTPRequestHandler(SimpleHTTPRequestHandler):

    def do_GET(self):

        url = f'https://{HOST}{self.path}'
        headers = dict(self.headers.items())
        headers.update({'Host': HOST})

        response = requests.get(url, headers=headers, verify=True)
        content = response.content
        if not response:
            self.send_error(response.status_code, content.decode())
            return None

        if 'text/html' in response.headers.get('Content-Type', ''):
            content = Parser.process(content)
            response.headers.update({'Content-Length': str(len(content))})

        self.send_response(response.status_code)
        self._send_headers(response.headers)
        self.wfile.write(content)

    def _send_headers(self, headers):
        map(self.send_header, headers.items())
        self.end_headers()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', dest='port', type=int, default=9000)
    args = parser.parse_args(sys.argv[1:])

    print(f'Http server is starting on port {args.port}...')
    server_address = ('0.0.0.0', args.port)
    httpd = HTTPServer(server_address, ProxyHTTPRequestHandler)
    print('Http server is started successfully!')
    httpd.serve_forever()
