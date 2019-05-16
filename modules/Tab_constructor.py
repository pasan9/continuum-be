from music21 import converter,meter

def getAlphaTex(arrangement,file_path):

    alphaTex_string = ''

    song = converter.parse(file_path)
    song = song.parts[0]

    time_signature = song.timeSignature.ratioString

    for measure in song.measures(0, None):
        for event in measure.recurse().getElementsByClass(['Note','Chord','Rest']):
            print(event)

    return None