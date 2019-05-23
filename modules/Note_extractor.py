from modules import audio_to_midi_melodia
from modules import Chord_extractor
from definitions.config import Paths
#Paths
# audio_path = Paths.audio_path
# file_path = audio_path + 'sal_audio.mp3'

def extract_notes(file_path,style):
    extracted_notes = get_melody(file_path)
    if style == 'Lead':
        return extracted_notes
    else:
        chords = get_chords(file_path)
        for chord in chords:
            for note in chord:
                extracted_notes.append(note)
        return extracted_notes



def get_melody(file_path):
    return audio_to_midi_melodia.get_melody(file_path)

def get_chords(file_path):
    return Chord_extractor.extractChords(file_path)

