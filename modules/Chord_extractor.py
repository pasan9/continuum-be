from madmom.audio.chroma import DeepChromaProcessor
from madmom.features.chords import DeepChromaChordRecognitionProcessor
from madmom.processors import SequentialProcessor
from definitions.Note import Note

midi_dict = {'C':24,'C#':25,'D':26,'D#':27,'E':28,'F':29,'F#':30,'G':31,'G#':32,'A':33,'A#':34,'B':35}

dcp = DeepChromaProcessor()
decode = DeepChromaChordRecognitionProcessor()
chordrec = SequentialProcessor([dcp, decode])

def extractChords(file_path):
    chord_labels = chordrec(file_path)
    chord_array = []

    for label in chord_labels:
        chord_array.append(createChord(label[0],label[1],label[2]))

    return chord_array

def createChord(start_time,end_time,label):
    #label format is - A:min
    if label != 'N': #'N' if for no code
        label_arr = label.split(":")
        root = label_arr[0]
        quality = label_arr[1]

        if quality == 'maj':
            return createMajorTriad(root,start_time,end_time-start_time)
        else:
            return createMinorTriad(root,start_time,end_time-start_time)




def createMajorTriad(note,onset,duration):
    #Get note value
    root_val = midi_dict[note]+12
    #Build 3 note major triad | 1st iteration - 4 semitones apart, 2nd iteration - 3 semitones apart
    chord = []
    for i in range (1,4):
        if i == 1:
            value = root_val
            chord.append(Note(onset=onset,duration=duration,value=value))
        elif i == 2:
            #4 semitones up
            value = root_val + 4
            chord.append(Note(onset=onset, duration=duration, value=value))
        else:
            # 4+3 = 7 semitones up
            value = root_val + 7
            chord.append(Note(onset=onset, duration=duration, value=value))
    return chord

def createMinorTriad(note,onset,duration):
    # Get note value
    root_val = midi_dict[note]+12
    # Build 3 note Minor triad | 1st iteration - 3 semitones apart, 2nd iteration - 4 semitones apart
    chord = []
    for i in range(1, 4):
        if i == 1:
            value = root_val
            chord.append(Note(onset=onset, duration=duration, value=value))
        elif i == 2:
            # 3 semitones up
            value = root_val + 3
            chord.append(Note(onset=onset, duration=duration, value=value))
        else:
            # 3+4 = 7 semitones up
            value = root_val + 7
            chord.append(Note(onset=onset, duration=duration, value=value))
    return chord





