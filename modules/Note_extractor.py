from modules import audio_to_midi_melodia
from modules import Chord_extractor
import math
from definitions.config import Paths
#Paths
# audio_path = Paths.audio_path
# file_path = audio_path + 'sal_audio.mp3'

def extract_notes(file_path,style,guitar):
    extracted_notes = get_melody(file_path,guitar)
    if style == 'Lead':
        return extracted_notes
    else:
        chords = get_chords(file_path)
        for chord in chords:
            for note in chord:
                extracted_notes.append(note)
        return extracted_notes



def get_melody(file_path,guitar):
    guitar_range = guitar.get_range()
    melody = audio_to_midi_melodia.get_melody(file_path)
    transposed_melody = []
    for note in melody:
        transposed_melody.append(transpose_to_range(guitar_range,note))
    return transposed_melody

def get_chords(file_path):
    return Chord_extractor.extractChords(file_path)

def transpose_to_range(guitar_range,note):
    selected_range = guitar_range
    note_value = note.value

    if (selected_range[0] <= note_value <= selected_range[1]):
        return note

    elif (note_value < selected_range[0]):
        diff = selected_range[0] - note_value
        # There are 12 notes in an octave, round the difference to upper multiple of 12 and add to lower bound of range
        note.value = note_value + int(math.ceil(diff / 12.0)) * 12
        return note

    elif (note_value > selected_range[1]):
        diff = note_value - selected_range[1]
        note.value = note_value - int(math.ceil(diff / 12.0)) * 12  # Transpose down by octaves
        return note

