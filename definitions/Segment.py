class Segment:

    def __init__(self,style=None,notes=[]):
        self.style = style
        self.notes = notes
    #Returns sequence of MIDI valus of the Notes
    def get_flat_note_vals(self):
        note_arr = []
        for note in self.notes:
            note_arr.append(note.value)
        return note_arr
