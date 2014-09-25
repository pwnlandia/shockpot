import logger
logger.logging_setup()
from logger import LOGGER

import bottle
from bottle import request, response
import json
from util import get_hpfeeds_client


app = bottle.default_app()
LOGGER.info( 'Loading config file shockpot.conf ...')
app.config.load_config('shockpot.conf')
hpclient = get_hpfeeds_client(app.config)

def is_shellshock(headers):
    for name, value in headers:
        if '() {' in value:
            return True
    return False

def get_request_record():
    headers = [[name, value,] for name, value in request.headers.items()]

    return {
        'method': request.method,
        'url': request.url,
        'path': request.path,
        'query_string': request.query_string,
        'headers': headers,
        'source_ip': request.environ.get('REMOTE_ADDR'),
        'dest_port': request.environ.get('SERVER_PORT'),
        'dest_host': request.environ.get('SERVER_NAME'),
        'is_shellshock': is_shellshock(headers)
    }

def log_request(record):
    global hpclient
    req = json.dumps(record)
    LOGGER.info(req)

    if hpclient:
        hpclient.publish(app.config['hpfeeds.channel'], req)

@app.route('/')
@app.route('/<path:re:.+>')
@app.route('/', method="POST")
@app.route('/<path:re:.+>', method="POST")
def func(**kwargs):
    log_request(get_request_record())
    response.set_header('Server', app.config['headers.server'])
    return bottle.template('<b>{{title}}</b>!', title='Hello')

bottle.run(host=app.config['server.host'], port=int(app.config['server.port']))

