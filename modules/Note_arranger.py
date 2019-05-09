from madmom.io.midi import MIDIFile
from definitions.config import Paths

midi_path = Paths.midi_path

def make_midi(notes,tempo):
    #Accepts a list of note objects and creates a MIDI file
    notesArr = []
    for note in notes:
        notesArr.append([note.onset,note.value,note.duration,100])

    midi_arr = MIDIFile.from_notes(notesArr, tempo=tempo)
    midi_arr.save(midi_path + 'song.mid')
