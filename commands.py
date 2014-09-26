from logger import LOGGER

import requests
import socket
import re
import os

ping_check_re = re.compile(r'ping\s+(:?-c\s*(?P<count>\d+)\s+)(?P<host>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
wget_check_re = re.compile(r'wget\s+.*(?P<url>https?://[^\s;]+)')
curl_check_re = re.compile(r'curl\s+.*(?P<url>https?://[^\s;]+)')
telnet_check_re = re.compile(r'telnet\s+(?P<host>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(?P<port>\d+)')

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
            command = 'ping -c {} {}'.format(count, host)
            try:
                os.system(command)
            except Exception as e:
                LOGGER.error(e)
            return command, ''
            
        mat = wget_check_re.search(value)
        if mat:
            wget = mat.groupdict()
            url = wget['url']
            LOGGER.info('Performing wget request on {}'.format(url))
            data = ''
            try:
                resp = requests.get(url, headers={'User-Agent': 'Wget/1.13.4 (linux-gnu)'})
                data = resp.text
            except Exception as e:
                LOGGER.error(e)
            return 'wget {}'.format(url), data

        mat = curl_check_re.search(value)
        if mat:
            curl = mat.groupdict()
            url = curl['url']
            LOGGER.info('Performing curl request on {}'.format(url))
            try:
                resp = requests.get(url, headers={'User-Agent': 'curl/7.30.0'})
                data = resp.text
            except Exception as e:
                LOGGER.error(e)
            return 'curl {}'.format(url), data

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
