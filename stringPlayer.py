import mido
from mido import Message
import random
import time
import kissearutil

class StringPlayer:

    def __init__(self, lowerMidiLimit, upperMidiLimit, outPort):
        self.lowerMidiLimit = lowerMidiLimit
        self.upperMidiLimit = upperMidiLimit
        self.outPort = outPort
        self.minNoteDur = 0.5
        self.maxNoteDur = 1.2
        self.noteDur = None
        self.absNoteOne = None
        self.absNoteTwo = None
        self.absNoteThree = None
        self.promptText = "Enter intervals separated by one space."

    def chooseNotes(self):
        #randomly choose intervals and notes
        intervalOne = random.randint(1, 12) * random.choice([-1, 1])
        intervalTwo = random.randint(1, 12) * random.choice([-1, 1])
        relNoteOne = 0
        relNoteTwo = relNoteOne + intervalOne
        relNoteThree = relNoteTwo + intervalTwo
        lowest = min([relNoteOne, relNoteTwo, relNoteThree])
        highest = max([relNoteOne, relNoteTwo, relNoteThree])
        noteRange = highest - lowest
        lowNote = random.randint(self.lowerMidiLimit, self.upperMidiLimit - noteRange)
        self.absNoteOne = lowNote + (lowest * -1)
        self.absNoteTwo = self.absNoteOne + intervalOne
        self.absNoteThree = self.absNoteTwo + intervalTwo

        #randomly choose note duration
        self.noteDur = random.uniform(self.minNoteDur, self.maxNoteDur)

        #return answer strings
        return [kissearutil.midiToDiatonic(abs(intervalOne)), kissearutil.midiToDiatonic(abs(intervalTwo))]

    def playNotes(self):
        #create messages
        msgOne = Message('note_on', note=self.absNoteOne, velocity=127)
        msgTwo = Message('note_on', note=self.absNoteTwo, velocity=127)
        msgThree = Message('note_on', note=self.absNoteThree, velocity=127)

        #play notes
        self.port.send(msgOne)
        time.sleep(self.noteDur)
        self.port.send(Message('note_off', note=self.absNoteOne))

        self.port.send(msgTwo)
        time.sleep(self.noteDur)
        self.port.send(Message('note_off', note=self.absNoteTwo))

        self.port.send(msgThree)
        time.sleep(self.noteDur)
        port.send(Message('note_off', note=self.absNoteThree))
