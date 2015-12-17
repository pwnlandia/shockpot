import hpfeeds
from logger import LOGGER
import psycopg2
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

def get_postgresql_handler(config):
    dbh = None
    if config['postgresql.enabled'].lower() == 'true':
        LOGGER.info('postgresql enabled, creating connection to {}:{}'.format(config['postgresql.host'], config['postgresql.port']))
        dbh = psycopg2.connect(database=config['postgresql.database'], user=config['postgresql.user'], password=config['postgresql.password'], host=config['postgresql.host'], port=config['postgresql.port'])
        cursor = dbh.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS 
                            connections	(
                            connection SERIAL PRIMARY KEY,
                            method TEXT, 
                            url TEXT, 
                            path TEXT, 
                            query_string TEXT,
                            headers TEXT,
                            source_ip TEXT,
                            source_port INTEGER,  
                            dest_host TEXT,
                            dest_port INTEGER, 
                            is_shellshock TEXT,
                            command TEXT,
                            command_data TEXT,
                            timestamp INTEGER
        );""")
        dbh.commit()
    else:
        LOGGER.info( 'postgresql is disabled')
    return dbh

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
