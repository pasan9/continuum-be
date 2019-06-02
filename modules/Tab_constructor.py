import music21
import definitions.Note
import definitions.Segment


def getAlphaTex(score, arrangement, style):
    # alphaTex_string = '\\title Test Title \n .\n'
    # alphaTex = ''
    # time_signature = score.timeSignature.ratioString
    alphaTexMeasures = []
    # 5 events per bar
    measures = []
    events = []
    for i, event in enumerate(score):
        events.append(event)
        if (i != 0 and i % 5 == 0) or i == len(score) - 1:
            measures.append(events)
            events = []
    # Create AlphaTex
    for measure in measures:
        alphaTex_string = ''
        for event in measure:
            if (isinstance(event, definitions.Note.Note)):
                fret = arrangement[event.id][1]
                string = 6 - arrangement[event.id][0]  # Assuming 6 String Guitar
                duration = 2
                alphaTex_string += '%s.%s.%s ' % (fret, string, duration)
            else:
                # Event is a chord
                duration = 2
                chord_string = '('
                for note in event.notes:
                    fret = arrangement[note.id][1]
                    string = 6 - arrangement[note.id][0]  # Assuming 6 String Guitar
                    chord_string += '%s.%s ' % (fret, string)
                ending_string = ').%s ' % (duration)
                chord_string = chord_string.strip() + ending_string
                alphaTex_string += chord_string
        alphaTexMeasures.append(alphaTex_string)
        alphaTex_final_string = ' |\n'.join(alphaTexMeasures)


    print(alphaTex_final_string)
    return alphaTex_final_string
