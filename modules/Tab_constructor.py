from music21 import converter,meter,note

def getAlphaTex(score,arrangement):

    #alphaTex_string = '\\title Test Title \n .\n'
    #alphaTex = ''

    alphaTexMeasures = []

    time_signature = score.timeSignature.ratioString


    for measure in score.measures(0, None):
        alphaTex_string = ''
        for event in measure.recurse().getElementsByClass('Note'):
            if (isinstance(event,note.Note)):
                fret = arrangement[event.id][1]
                string = 6-arrangement[event.id][0] #Assuming 6 String Guitar
                #duration = event.duration.quarterLength
                duration = 2
                #print('fret - %s , string - %s, duration - %s',fret,string,duration)
                alphaTex_string += '%s.%s.%s '%(fret,string,duration)
        alphaTexMeasures.append(alphaTex_string)

    alphaTex_final_string = ' |\n'.join(alphaTexMeasures)

    print(alphaTex_final_string)
    return None