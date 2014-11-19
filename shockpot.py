
import logger
logger.logging_setup()
from logger import LOGGER

import bottle
from bottle import request, response
import json
from util import get_hpfeeds_client, get_ext_ip
from commands import perform_commands
import re
import datetime
import urlparse

shellshock_re = re.compile(r'\(\s*\)\s*{')

# this is the default apache page
page_template = '''<html><body><h1>{{title}}</h1>
<p>This is the default web page for this server.</p>
<p>The web server software is running but no content has been added, yet.</p>
</body></html>
'''

app = bottle.default_app()
LOGGER.info( 'Loading config file shockpot.conf ...')
app.config.load_config('shockpot.conf')
hpclient = get_hpfeeds_client(app.config)

public_ip = None
if app.config['fetch_public_ip.enabled'].lower() == 'true':
    public_ip = get_ext_ip(json.loads(app.config['fetch_public_ip.urls']))
    print 'public_ip =', public_ip

def is_shellshock(headers):
    for name, value in headers:
        if shellshock_re.search(value):
            return True
    return False

def get_request_record():
    headers = [[name, value,] for name, value in request.headers.items()]
    is_shellshock_check = is_shellshock(headers)
    
    command, data = None, None
    if is_shellshock_check:
        command, data = perform_commands(headers)

    if public_ip:
        dest_host = public_ip
    else:
        dest_host = urlparse.urlparse(request.url).netloc.split(':',1)[0]

    return {
        'method': request.method,
        'url': request.url,
        'path': request.path,
        'query_string': request.query_string,
        'headers': headers,
        'source_ip': request.environ.get('REMOTE_ADDR'),
        'dest_port': request.environ.get('SERVER_PORT'),
        'dest_host': dest_host,
        'is_shellshock': is_shellshock_check,
        'command': command,
        'command_data': data,
        'timestamp': str(datetime.datetime.now())
    }

def log_request(record):
    global hpclient
    req = json.dumps(record)
    LOGGER.info(req)

    if hpclient and record['is_shellshock']:
        hpclient.publish(app.config['hpfeeds.channel'], req)

@app.route('/')
@app.route('/<path:re:.+>')
@app.route('/', method="POST")
@app.route('/<path:re:.+>', method="POST")
def func(**kwargs):
    log_request(get_request_record())
    response.set_header('Server', app.config['headers.server'])
    return bottle.template(page_template, title='It works!')

bottle.run(host=app.config['server.host'], port=int(app.config['server.port']))

