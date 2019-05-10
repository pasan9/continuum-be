from modules import Note_extractor,Note_arranger,Note_locator
from definitions.config import Paths
from definitions.Guitar import Guitar
import librosa

midi_path = Paths.midi_path
audio_path = Paths.audio_path
file_path = audio_path + 'sal_audio.mp3'
midi_file_path = midi_path+'song.mid'

#Get Song tempo
y, sr = librosa.load(file_path)
tempo, beat_frames = librosa.beat.beat_track(y=y,sr=sr)


notes = Note_extractor.get_melody(file_path)

#Create the midi file from notes
Note_arranger.make_midi(notes,tempo)

guitar = Guitar(6,24)

Note_locator.arrange(guitar,midi_file_path,'lead')






print(notes)