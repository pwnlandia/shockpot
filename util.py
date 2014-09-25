import hpfeeds
from logger import LOGGER

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
