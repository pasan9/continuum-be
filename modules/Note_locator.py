from definitions.config import Paths
from definitions.Note import Note
from definitions.Segment import Segment
from music21 import converter, corpus, instrument, midi, note, chord, pitch

midi_path = Paths.midi_path



def segment_midi(file_path,style):
    #score = open_midi(path)
    song = converter.parse(file_path)
    song = song.parts[0]
    segments = []
    for measure in song.measures(0, None):
        segment = Segment(style='seq',notes=[])
        for note in measure.recurse().getElementsByClass('Note'):
            print(note.id)
            segment.notes.append(Note(id=note.id,value=note.pitch.midi))
        segments.append(segment)
    return segments

    # song.write("midi", midi_path+'m21midi.mid')

def arrange(guitar,segments):
    #Represent each note with {id:position}
    complete_arrangement = dict()



def arrange_seq(segment,previous_segment,complete_arrangement):


    return None

def arrange_chord():
    return None









# def open_midi(midi_path):
#     mf = midi.MidiFile()
#     mf.open(midi_path)
#     mf.read()
#     mf.close()
#     return midi.translate.midiFileToStream(mf)
