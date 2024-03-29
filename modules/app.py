from flask import Flask, request, redirect, url_for, Response
from modules import Note_extractor,Note_arranger,Note_locator,MIDI_synth,Tab_constructor
from definitions.config import Paths
from definitions.Guitar import Guitar
import librosa
import os
import tempfile
from werkzeug.utils import secure_filename
import json
import base64


midi_path = Paths.midi_path
audio_path = Paths.audio_path
file_path = audio_path + 'sal_audio.mp3'
midi_file_path = midi_path+'song.mid'
gen_audio_path = Paths.generated_audio_path
gen_audio_file_path = gen_audio_path+'song.mp3'

UPLOAD_FOLDER = '/home/pasan/Projects/continuum-final/audio'
ALLOWED_EXTENSIONS = set(['wav','mp3'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/test",methods=['GET'])
def test():
    tabs = arrangeSong(file_path)
    return tabs



@app.route("/arrange",methods=['POST'])
def upload_file():
    rx = request
    tmp = tempfile.gettempdir()
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No File!')
            return 'No File'
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('Empty File!')
            return 'Empty File'
        if file and allowed_file(file.filename):
            #filename = 'temp.mp3'
            filename = secure_filename(file.filename)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            #Generate Arrangement

            style = request.form.get('playing_style')

            midi_encoded,tabString = arrangeSong(app.config['UPLOAD_FOLDER']+'/'+filename,style)

            resp = construct_response({'tab_string':tabString,'midi_encoded':midi_encoded},200)

            return resp
    return None

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def arrangeSong(file_path,style):

    #Get Song tempo
    y, sr = librosa.load(file_path)
    tempo, beat_frames = librosa.beat.beat_track(y=y,sr=sr)

    guitar = Guitar(6,10)

    notes = Note_extractor.extract_notes(file_path,style,guitar)

    #Create the midi file from notes
    Note_arranger.make_midi(notes,tempo)

    # MIDI_synth.writeAudio(midi_file_path,gen_audio_file_path)

    score,arrangement = Note_locator.arrange(guitar,midi_file_path,style)

    #Convert the midi file to base 64
    encoded_string = ""
    with open(midi_file_path, "rb") as midi_file:
        encoded_string = base64.b64encode(midi_file.read()).decode("utf-8")

    tab_string = Tab_constructor.getAlphaTex(score,arrangement,style)


    return encoded_string,tab_string

def construct_response(data,status):
    json_data = json.dumps(data)
    resp = Response(json_data,status=status, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# UPLOAD_FOLDER = '/path/to/the/uploads'
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
#
# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



