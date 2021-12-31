# Speech to text app
Simple speech to text Flask app for Windows
- Free
- Simple to install and use

# Install steps
- **Install Python 3.x**: [install python](https://www.python.org/downloads/)
- **Download the code**: [Download ZIP](https://github.com/TraxData313/speech-to-text-app/archive/refs/heads/main.zip) then unzip or clone this repo
- **Install requirements**: Open command promt from speech-to-text-app directory and run command: `pip install -r ./requirements.txt`

# Usage
- **Upload your data**: Create a folder named `data` inside the speech-to-text-app directory and place the wav files you want to convert to text there
- ![image](https://user-images.githubusercontent.com/45358654/147816270-86077d8a-1c6d-4e4e-9eb7-e14eeeecb0d5.png)
- **Run Flask**: Open command promt from speech-to-text-app directory, run command `flask run` and leave the command promt windows open
- **Open the GUI**: Open a browser and go to address: `http://127.0.0.1:5000/`
- **Speech-to-text**: Follow the instructions on the GUI to turn your wav file to text
![image](https://user-images.githubusercontent.com/45358654/147816362-411dc470-b2da-47d2-9d54-61a3def474db.png)
- **Stop the app**: When done using the app, close the command promt window that runs the command `flask run`
