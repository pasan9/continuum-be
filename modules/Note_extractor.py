from modules import audio_to_midi_melodia
from definitions.config import Paths
#Paths
# audio_path = Paths.audio_path
# file_path = audio_path + 'sal_audio.mp3'

def get_melody(file_path):
    return audio_to_midi_melodia.get_melody(file_path)

