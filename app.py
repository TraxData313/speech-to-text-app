# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
import logging, traceback 
from logging.handlers import RotatingFileHandler
import time, atexit
import os
import speech_recognition as sr

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
def speech_to_text(file_name, adjust_for_noice=False, show_all=False, language="en-US"):
    file_name = f'data/{file_name}'
    if os.path.exists(file_name):
        r = sr.Recognizer()
        data = sr.AudioFile(file_name)
        with data as source:
            if adjust_for_noice:
                r.adjust_for_ambient_noise(source)
            audio = r.record(source)
        responce = r.recognize_google(audio, show_all=show_all, language=language)
    else:
        responce = f'<b style="color:red">ERROR</b>: File [{file_name}] does not exist! Make sure it is in the available files list!'
    return responce
###################################
# END FUNCTIONS
###################################



@app.route('/', methods=['GET', 'POST'])
def home():
    title = 'STT: Home'
    form_responce = 'none'
    txt_from_speech = 'the speech as text will be shown here'
    available_files = os.listdir("data")
    # Form:
    if request.method == 'POST':
        try:
            boxes = request.form.getlist('mycheckbox')
            form_responce = boxes
            file_name = boxes[0]
            language = boxes[1]
            adjust_for_noice = bool(int(boxes[2]))
            show_all = bool(int(boxes[3]))
            txt_from_speech = speech_to_text(file_name, adjust_for_noice, show_all, language)
        except Exception as e:
            txt_from_speech = f'<b style="color:red">ERROR</b>: [{e}]'
    return render_template(
        'index.html', 
        title=title,
        form_responce=form_responce,
        available_files=available_files,
        txt_from_speech=txt_from_speech
        )



if __name__ == "__main__":
    try:
        app.logger.info('Starting Speech to text app...')
        app.run(host='0.0.0.0',port=8000)
    except Exception as e:
        app.logger.error(str(traceback.format_exc()))