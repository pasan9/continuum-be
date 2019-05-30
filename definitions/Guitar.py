import numpy as np
import random
import math

class Guitar:
    # Standard Tuning in MIDI
    standard_tuning_midi = [64, 59, 55, 50, 45, 40]

    def __init__(self, n_strings, n_frets):
        self.n_strings = n_strings
        self.n_frets = n_frets
        self.fretboard = self.generate_fretboard(self.standard_tuning_midi, self.n_frets)

    # Creates the fretboard
    def generate_fretboard(self, string_vals, n_frets):
        fretboard = []

        for val in string_vals:
            fret_values = np.arange(val, val + n_frets + 1)
            fretboard.append(fret_values)

        return np.matrix(fretboard)

    # Returns positions of a given note
    def get_positions(self, note_val):
        result = np.where(self.fretboard == note_val)
        # Return as a list of coordinates
        return list(zip(result[0], result[1]))

    def get_random_position(self,note_val):
        return random.choice(self.get_positions(note_val))

    def get_note_from_position(self,position):
        return self.fretboard.item(position)

    def get_range(self):
        lower_bound = self.fretboard.min()
        upper_bound = self.fretboard.max()
        return (lower_bound,upper_bound)

    def find_frontmost(self,note_val):
        positions = self.get_positions(note_val)
        min_position = positions[0]

        for position in positions:
            if (position[0]<min_position[0]):
                min_position = position

        return min_position

    def find_nearest(self,note_val,prev_position):
        if prev_position is None:
            return self.find_frontmost(note_val)

        positions = self.get_positions(note_val)
        min_position = positions[0]
        for position in positions:
            current_dis = self.get_euc_distance(min_position,prev_position)
            new_dis = self.get_euc_distance(position,prev_position)
            if(new_dis < current_dis):
                min_position = position

        return min_position


    def get_euc_distance(self,pos1,pos2):
        distance = math.sqrt(((pos1[0] - pos2[0]) ** 2) + ((pos1[1] - pos2[1]) ** 2))
        return distance




