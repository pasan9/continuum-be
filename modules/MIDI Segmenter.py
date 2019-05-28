#!/usr/bin/env python
# coding: utf-8

# In[1]:


midi_path = 'audio/midi/'
file = midi_path + 'song.mid'


# In[2]:


class Note:

    def __init__(self,onset=0,duration=0,value=0,id=None,position=None):
        self.id = id
        self.position = position
        self.onset = onset
        self.duration = duration
        self.value = value

class Segment:

    def __init__(self,style=None,notes=None):
        self.style = style
        self.notes = notes
    #Returns sequence of MIDI valus of the Notes
    def get_flat_note_vals(self):
        note_arr = []
        for note in self.notes:
            note_arr.append(note.value)
        return note_arr


# In[3]:


import mido
mid = mido.MidiFile(file)


# In[4]:


# for i, track in enumerate(mid.tracks):
#     print('Track {}: {}'.format(i, track.name))
#     for msg in track:
#         print(msg)

#Converting MIDI events to note objects

notes = []
track = mid.tracks[0]
real_time = 0
for msg in track:
    if isinstance(msg,mido.messages.messages.Message):
        real_time += msg.time
        if (msg.type=='note_on'):
            #print(real_time,msg.note)
            notes.append(Note(onset=real_time,value=msg.note))
        #print(msg.note,msg.time)
        #print(msg.type)
        #print(type(msg))
        #print(dir(msg))


# In[5]:


#Note and chord segmentation
events = []
current_events = []
current_time = 0
for note in notes:
    if (note.onset == current_time):
        current_events.append(note)
    else:
        if (len(current_events)>1):
            events.append(Segment(style='cho',notes=current_events))
            current_events = [note]
        elif(current_events):
            events.append(current_events[0])
            current_events = [note]
        current_time = note.onset

        


# In[6]:


events


# In[ ]:




