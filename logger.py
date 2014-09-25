#!/usr/bin/env python

import logging
import logging.handlers
import os

LOGGER = logging.getLogger('shockpot-logger')

def logging_setup():
    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(message)s')

    # File handler
    logfile = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'shockpot.log')
    fh = logging.handlers.RotatingFileHandler(logfile, 'a', 2097152, 10)
    fh.setFormatter(formatter)

    # Add handlers
    LOGGER.addHandler(fh)
   
    # Set level
    LOGGER.setLevel(logging.INFO)
    return True
