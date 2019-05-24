from definitions.config import Paths
from definitions.Note import Note
from definitions.Segment import Segment
from modules.Sequence_arranger import get_seq_placements
from modules.Chord_arranger import get_chord_placements
import music21
#from music21 import converter, corpus, instrument, midi, chord, pitch, stream, note


midi_path = Paths.midi_path

def readScore(file_path):
    mf = music21.midi.MidiFile()
    mf.open(file_path)
    mf.read()
    mf.close()

    score = music21.midi.translate.midiFileToStream(mf)

    #score = converter.parse(file_path)
    score = score.parts[0]

    #Tag all elements with a unique id
    id = 0
    for element in score.elements:
        #Notes and other elements
        element.id = id
        id += 1
        #Chords and notes inside them
        if isinstance(element, music21.chord.Chord):
            for note in element:
                note.id = id
                id += 1
        #Check if a normal element or a voice
        if isinstance(element, music21.stream.Voice):
            for innerElement in element:
                innerElement.id = id
                id += 1
                if isinstance(innerElement,music21.chord.Chord):
                    for note in innerElement:
                        note.id = id
                        id+=1
    return score

def segment_score(score,style):
    #Simply segment by measures for lead guitar
    if style == 'Lead':
        segments = []
        for measure in score.measures(0, None):
            segment = Segment(style='seq',notes=[])
            for note in measure.recurse().getElementsByClass('Note'):
                segment.notes.append(Note(id=note.id,value=note.pitch.midi))
            segments.append(segment)
        return segments
    else:
        mixed_segments = [] #Put Note events and chord segments to fully segment later
        for element in score.flat.elements:
            if isinstance(element,music21.note.Note):
                mixed_segments.append(Note(id=element.id,value=element.pitch.midi))
            elif isinstance(element,music21.chord.Chord):
                segment = Segment(style='cho', notes=[])
                for note in element:
                    segment.notes.append(Note(id=note.id, value=note.pitch.midi))
                mixed_segments.append(segment)

        #Find sequence segments and append
        segments = []
        seq_segment = Segment(style='seq', notes=[])
        for event in mixed_segments:
            if (isinstance(event, Note)):
                seq_segment.notes.append(event)
            else:
                if (seq_segment.notes):
                    if (len(seq_segment.notes) < 2):
                        event.notes.append(seq_segment.notes[0])
                    else:
                        segments.append(seq_segment)
                    seq_segment = Segment(style='seq', notes=[])
                segments.append(event)
        return segments



def arrange(guitar,file_path,style):

    score = readScore(file_path)

    segments = segment_score(score,style)

    #Represent each note with {id:position}
    complete_arrangement = []

    complete_arrangement_dict = dict()

    for segment in segments:
        # no_segments += 1
        # no_notes += len(segment)
        # Previous result : If first segment then set to None
        previous_segment = complete_arrangement and complete_arrangement[-1] or None
        if segment.style=="seq":
            # print(segment.notes)
            positions = get_seq_placements(guitar,segment.get_flat_note_vals(),previous_segment)
            complete_arrangement.append(positions)
        else :
            positions = get_chord_placements(guitar, segment.get_flat_note_vals(), previous_segment)
            complete_arrangement.append(positions)
        for note,position in zip(segment.notes, positions):
            complete_arrangement_dict[note.id] = position

            # for i in enumerate(segment.notes,positions):
            #     complete_arrangement_dict[segment.notes[i].id] = positions[i]

    # for segment in segments:
    #     for note in segment.notes:
    #         complete_arrangement_dict[note.id] = note.position

    return score,complete_arrangement_dict

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
