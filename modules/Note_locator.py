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
        segment = Segment(style='seq')
        for i,note in enumerate(score):
            segment.notes.append(note)
            if (i != 0 and i%5 == 0) or i == len(score)-1:
                segments.append(segment)
                segment = Segment(style='seq')
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

        if (len(segment.notes)<1):
            continue

        elif (len(segment.notes)<2):
            prev_position = previous_segment and previous_segment[-1] or None
            positions = [guitar.find_nearest(segment.notes[0].value,prev_position)]
            complete_arrangement.append(positions)

        elif segment.style=="seq":
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
