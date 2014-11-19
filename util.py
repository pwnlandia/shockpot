import hpfeeds
from logger import LOGGER
import socket
import requests
from requests.exceptions import Timeout, ConnectionError

import logging
logger = logging.getLogger(__name__)

def get_hpfeeds_client(config):
    hpc = None
    if config['hpfeeds.enabled'].lower() == 'true':
        LOGGER.info('hpfeeds enabled, creating connection to {}:{}'.format(config['hpfeeds.host'], config['hpfeeds.port']))
        hpc = hpfeeds.new(
            config['hpfeeds.host'], 
            int(config['hpfeeds.port']), 
            config['hpfeeds.identity'], 
            config['hpfeeds.secret']
        )
        hpc.s.settimeout(0.01)
    else:
        LOGGER.info( 'hpfeeds is disabled')
    return hpc

def valid_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except:
        return False

def get_ext_ip(urls):
    for url in urls:
        try:
            req = requests.get(url)
            if req.status_code == 200:
                data = req.text.strip()
                if data is None or not valid_ip(data):
                    continue
                else:
                    return data
            else:
                raise ConnectionError
        except (Timeout, ConnectionError) as e:
            logger.warning('Could not fetch public ip from {0}'.format(url))
    return None
