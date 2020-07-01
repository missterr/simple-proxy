#!/usr/bin/env python

import argparse
import re
import sys
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from itertools import cycle

import requests

HOST = 'lifehacker.ru'
EMOJI = ('\U0001F606', '\U0001f600', '\U0001F606', '\U0001F923')


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
            content = self._add_emoji(content)
            response.headers.update({'Content-Length': str(len(content))})

        self.send_response(response.status_code)
        self._send_headers(response.headers)
        self.wfile.write(content)

    def _send_headers(self, headers):
        map(self.send_header, headers.items())
        self.end_headers()

    @staticmethod
    def _add_emoji(content: bytes) -> bytes:
        pattern = r'(\b[а-яА-Я]{6})([.,\/#!$%\^&\*;:{}=\-_`~()«»<>\s])'
        compiled = re.compile(pattern)

        def callback(match, emoji):
            return f'{match.group(1)}{next(emoji)}{match.group(2)}'

        callback = partial(callback, emoji=cycle(EMOJI))
        processed = compiled.sub(callback, content.decode())

        return processed.encode()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', dest='port', type=int, default=9000)
    args = parser.parse_args(sys.argv[1:])

    print(f'Http server is starting on port {args.port}...')
    server_address = ('127.0.0.1', args.port)
    httpd = HTTPServer(server_address, ProxyHTTPRequestHandler)
    print('Http server is started successfully!')
    httpd.serve_forever()
