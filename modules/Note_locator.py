from definitions.config import Paths
from definitions.Note import Note
from definitions.Segment import Segment
from modules.Sequence_arranger import get_seq_placements
from modules.Chord_arranger import get_chord_placements
import music21
import mido
#from music21 import converter, corpus, instrument, midi, chord, pitch, stream, note


midi_path = Paths.midi_path

def readScore(file_path,style):

    if (style=='Lead'):
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
    else:
        mid = mido.MidiFile(file_path)
        notes = []
        track = mid.tracks[0]
        real_time = 0
        #Put all notes to a mixed
        msgId = 0
        for msg in track:
            if isinstance(msg, mido.messages.messages.Message):
                real_time += msg.time
                if (msg.type == 'note_on'):
                    notes.append(Note(onset=real_time, value=msg.note,id=msgId))
                    msgId += 1
        return notes



def segment_score(score,style):
    #Simply segment by measures for lead guitar
    if style == 'Lead':
        segments = []
        for measure in score.measures(0, None):
            #x = len(measure.recurse().getElementsByClass('Note'))
            segment = Segment(style='seq',notes=[])
            for note in measure.recurse().getElementsByClass('Note'):
                segment.notes.append(Note(id=note.id,value=note.pitch.midi))
            segments.append(segment)
        return segments
    else:
        mixed_segments = [] #Put Note events and chord segments to fully segment later
        current_events = []
        current_time = 0
        for i,note in enumerate(score):
            if (note.onset == current_time):
                current_events.append(note)
            else:
                if (len(current_events) > 1):
                    mixed_segments.append(Segment(style='cho', notes=current_events))
                    current_events = [note]
                elif (current_events):
                    mixed_segments.append(current_events[0])
                    current_events = [note]
                current_time = note.onset
            if (i == len(score) - 1):
                if (len(current_events) > 1):
                    mixed_segments.append(Segment(style='cho', notes=current_events))
                elif (current_events):
                    mixed_segments.append(current_events[0])


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
        return segments,mixed_segments



def arrange(guitar,file_path,style):

    score = readScore(file_path,style)

    if (style == 'Lead'):
        segments = segment_score(score,style)
    else:
        segments,score = segment_score(score,style)

    #Represent each note with {id:position}
    complete_arrangement = []

    complete_arrangement_dict = dict()

    for segment in segments:
        # no_segments += 1
        # no_notes += len(segment)
        # Previous result : If first segment then set to None
        previous_segment = complete_arrangement and complete_arrangement[-1] or None
        if segment.style=="seq":
            positions = get_seq_placements(guitar,segment.get_flat_note_vals(),previous_segment)
            complete_arrangement.append(positions)
        else :
            positions = get_chord_placements(guitar, segment.get_flat_note_vals(), previous_segment)
            complete_arrangement.append(positions)

        for note,position in zip(segment.notes, positions):
            complete_arrangement_dict[note.id] = position

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
