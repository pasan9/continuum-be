from definitions.config import Paths
from definitions.Note import Note
from definitions.Segment import Segment
from modules.Sequence_arranger import get_seq_placements
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

def arrange(guitar,file_path,style):

    segments = segment_midi(file_path,style)

    #Represent each note with {id:position}
    complete_arrangement = []

    for segment in segments:
        # no_segments += 1
        # no_notes += len(segment)
        # Previous result : If first segment then set to None
        previous_segment = complete_arrangement and complete_arrangement[-1] or None
        if segment.style=="seq":
            complete_arrangement.append(get_seq_placements(guitar,segment,previous_segment))
            # print(plc)

    complete_arrangement_dict = dict()

    for segment in complete_arrangement:
        for note in segment:
            complete_arrangement_dict[note.id] = note.position

    return complete_arrangement_dict

        #complete_arrangement.append(get_placements(guitar,segment, previous_result, style))
    #
    # print('No. of Segments :',no_segments)
    # print('No. of Notes :', no_notes)
    # print('Time Elapsed :', time.time() - start_time)
    #return complete_arrangement









# def open_midi(midi_path):
#     mf = midi.MidiFile()
#     mf.open(midi_path)
#     mf.read()
#     mf.close()
#     return midi.translate.midiFileToStream(mf)
