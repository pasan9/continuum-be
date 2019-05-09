class Note:

    def __init__(self,onset=0,duration=0,value=0,id=None,position=None):
        self.id = id
        self.position = position
        self.onset = onset
        self.duration = duration
        self.value = value
