# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
import logging, traceback 
from logging.handlers import RotatingFileHandler
import time, atexit
import os

app = Flask(__name__)

# LOGGERs:
def init_logger():
    logger = logging.getLogger('SPEECH-TO-TEXT')
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.setLevel(level=logging.DEBUG)
    # add a log rotating handler (rotates when the file becomes 10MB, or about 100k lines):
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler = RotatingFileHandler('logs/messages.log', maxBytes=10000000, backupCount=10)
    handler.setLevel(level=logging.DEBUG)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
app.logger = init_logger()



###################################
# VARIABLES AND PARAMS:
###################################
app.some_param = None
###################################
# END VARIABLES AND PARAMS
###################################



###################################
# FUNCTIONS:
###################################
app.some_param = None
###################################
# END FUNCTIONS
###################################



@app.route('/', methods=['GET', 'POST'])
def home():
    title = 'STT: Home'

    return render_template(
        'index.html', 
        title=title
        )



if __name__ == "__main__":
    try:
        app.logger.info('Starting Speech to text app...')
        app.run(host='0.0.0.0',port=8000)
    except Exception as e:
        app.logger.error(str(traceback.format_exc()))