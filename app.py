# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
import logging, traceback 
from logging.handlers import RotatingFileHandler
import os, io
import speech_recognition as sr
from google.cloud import speech
from google.oauth2 import service_account


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
def _get_google_json_filename(folder='./google_api_key'):
    jsons = [file for file in os.listdir(folder) if '.json' in file]
    if len(jsons) == 0:
        message = """ERROR: JSON files with Google Cloud credentionas not found! There were 0 JSON files in the ./google_api_key directory.
        
Please follow the "Setting up authentication" part of this instruction https://cloud.google.com/speech-to-text/docs/libraries#setting_up_authentication to generate the JSON file and place it inside the ./google_api_key directory then retry."""
        raise Exception(message)
    elif len(jsons) > 1:
        message = """ERROR: Ambiguous credentions file! There were multiple JSON files in the ./google_api_key directory.
        
Please leave only one JSON file in the ./google_api_key directory containing your google cloud credentians as generated per the "Setting up authentication" part of this instruction https://cloud.google.com/speech-to-text/docs/libraries#setting_up_authentication.
"""
        raise Exception(message)
    else:
        return f'{folder}/{jsons[0]}'

def speech_to_text_gfree(file_name, adjust_for_noice=False, show_all=False, language="en-US"):
    try:
        file_name = f'data/{file_name}'
        if os.path.exists(file_name):
            r = sr.Recognizer()
            data = sr.AudioFile(file_name)
            with data as source:
                if adjust_for_noice:
                    r.adjust_for_ambient_noise(source)
                audio = r.record(source)
            response = r.recognize_google(audio, show_all=show_all, language=language)
        else:
            response = f'<b style="color:red">ERROR</b>: File [{file_name}] does not exist! Make sure it is in the available files list!'
        return response
    except Exception as e:
        app.logger.error(str(traceback.format_exc()))
        return f"{e}"

def speech_to_text_gcloud(file_name, show_all=False, language="en-US"):
    try:
        file_name = f'data/{file_name}'
        if os.path.exists(file_name):
            r = sr.Recognizer()
            data = sr.AudioFile(file_name)
            with data as source:
                audio = r.record(source)
            # Client:
            try:
                client = speech.SpeechClient()
            except:
                credentials = service_account.Credentials.from_service_account_file(_get_google_json_filename())
                client = speech.SpeechClient(credentials=credentials)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code=language,
            )
            # Detects speech in the audio file
            response = client.recognize(config=config, audio=audio)
            if show_all:
                for result in response.results:
                    response = "Transcript: {}".format(result.alternatives[0].transcript)
        else:
            response = f'<b style="color:red">ERROR</b>: File [{file_name}] does not exist! Make sure it is in the available files list!'
        return response
    except Exception as e:
        app.logger.error(str(traceback.format_exc()))
        return f"{e}"

###################################
# END FUNCTIONS
###################################



@app.route('/', methods=['GET', 'POST'])
def home():
    title = 'STT: Home'
    form_response = 'none'
    txt_from_speech = 'the speech as text will be shown here'
    available_files = os.listdir("data")
    # Form:
    if request.method == 'POST':
        try:
            boxes = request.form.getlist('mycheckbox')
            form_response = boxes
            file_name = boxes[0]
            engine = int(boxes[1])
            language = boxes[2]
            adjust_for_noice = bool(int(boxes[3]))
            show_all = bool(int(boxes[4]))
            if engine == 0:
                txt_from_speech = speech_to_text_gfree(file_name, adjust_for_noice, show_all, language)
            elif engine == 1:
                txt_from_speech = speech_to_text_gcloud(file_name, show_all, language)
        except Exception as e:
            txt_from_speech = f'<b style="color:red">ERROR</b>: [{e}]'
    return render_template(
        'index.html', 
        title=title,
        form_response=form_response,
        available_files=available_files,
        txt_from_speech=txt_from_speech
        )



if __name__ == "__main__":
    try:
        app.logger.info('Starting Speech to text app...')
        app.run(host='0.0.0.0',port=8000)
    except Exception as e:
        app.logger.error(str(traceback.format_exc()))