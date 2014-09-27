from logger import LOGGER

import requests
import socket
import re
import subprocess

ping_check_re = re.compile(r'ping\s+(:?-c\s*(?P<count>\d+)\s+)(?P<host>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
wget_check_re = re.compile(r'wget\s+.*(?P<url>https?://[^\s;]+)')
curl_check_re = re.compile(r'curl\s+.*(?P<url>https?://[^\s;]+)')
wget_check_re2 = re.compile(r'wget\s+(.*\s+)?(?P<url>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(:\d+)?/[^\s;]+)')
curl_check_re2 = re.compile(r'curl\s+(.*\s+)?(?P<url>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(:\d+)?/[^\s;]+)')

telnet_check_re = re.compile(r'telnet\s+(?P<host>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(?P<port>\d+)')


USER_AGENTS = {
    'wget': 'Wget/1.13.4 (linux-gnu)',
    'curl': 'curl/7.30.0',
}

def web_request(program, url):
    LOGGER.info('Performing {} request on {}'.format(program, url))
    data = ''
    try:
        resp = requests.get(url, headers={'User-Agent': USER_AGENTS[program]})
        data = resp.text
    except Exception as e:
        LOGGER.error(e)
    return '{} {}'.format(program, url), data

def perform_commands(headers):
    for name, value in headers:
        mat = ping_check_re.search(value)
        if mat:
            # do ping
            ping = mat.groupdict()
            # don't do more than 20 pings
            count = min(20, int(ping.get('count', 1)))
            host = ping['host']
            LOGGER.info('Performing {} pings against {}'.format(count, host))

            # host must match an IP regex and count must be a number, prevents command injection here
            command = ['ping', '-n', '-c', str(count), host]
            try:
                subprocess.call(command)
            except Exception as e:
                LOGGER.error(e)
            return ' '.join(command), ''
            
        mat = wget_check_re.search(value)
        if mat:
            return web_request('wget', mat.groupdict()['url'])

        mat = wget_check_re2.search(value)
        if mat:
            return web_request('wget', 'http://'+mat.groupdict()['url'])

        mat = curl_check_re.search(value)
        if mat:
            return web_request('curl', mat.groupdict()['url'])

        mat = curl_check_re2.search(value)
        if mat:
            return web_request('curl', 'http://'+mat.groupdict()['url'])

        mat = telnet_check_re.search(value)
        if mat:
            telnet = mat.groupdict()
            try:
                host = telnet['host']
                port = telnet['port']
                LOGGER.info('Openning socket to {}:{}'.format(host, port))
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((host, int(port)))
                s.close()
            except Exception as e:
                LOGGER.error(e)
            return 'telnet {}'.format(host, port), ''
    return None, None
