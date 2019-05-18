from music21 import converter,meter,note

def getAlphaTex(score,arrangement):

    alphaTex_string = '\\title Test Title \n'


    time_signature = score.timeSignature.ratioString


    for measure in score.measures(0, None):
        for event in measure.recurse().getElementsByClass('Note'):
            if (isinstance(event,note.Note)):
                fret = arrangement[event.id][1]
                string = 6-arrangement[event.id][0] #Assuming 6 String Guitar
                duration = event.duration.quarterLength
                #print('fret - %s , string - %s, duration - %s',fret,string,duration)
                alphaTex_string += '%s.%s '%(fret,string)
        alphaTex_string += "|\n"
    print(alphaTex_string)
    return None