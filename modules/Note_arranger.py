import mido
from madmom.io.midi import MIDIFile
from definitions.config import Paths

midi_path = Paths.midi_path

def make_midi(notes,tempo):
    #Accepts a list of note objects and creates a MIDI file
    notesArr = []
    for note in notes:
        notesArr.append([note.onset,note.value,note.duration,100])

    midi_obj = MIDIFile.from_notes(notesArr, tempo=tempo)

    #Instrument meta message
    #meta_ins = mido.MetaMessage('instrument_name', name='acoustic guitar (nylon)', time=0)
    ins_msg = mido.Message('program_change',program=25)
    midi_obj.tracks[0].insert(0, ins_msg)

    midi_obj.save(midi_path + 'song.mid')
