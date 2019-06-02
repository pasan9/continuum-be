from midi2audio import FluidSynth

def writeAudio(midi_path,gen_audio_path):
    fs = FluidSynth()
    fs.midi_to_audio(midi_path,gen_audio_path)