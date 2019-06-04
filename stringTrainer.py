import mido
from mido import Message
import random
import time
import kissearutil

class StringTrainer:

    def __init__(self):
        self.minNoteDur = 0.5
        self.maxNoteDur = 1.2
        self.noteDur = None
        self.absNoteOne = None
        self.absNoteTwo = None
        self.absNoteThree = None
        self.intervalOneAnswer = None
        self.intervalTwoAnswer = None
        self.promptText = "Enter intervals separated by one space."

    def chooseNotes(self, lowerMidiLimit, upperMidiLimit):
        #randomly choose intervals and notes
        intervalOne = random.randint(1, 12) * random.choice([-1, 1])
        intervalTwo = random.randint(1, 12) * random.choice([-1, 1])
        relNoteOne = 0
        relNoteTwo = relNoteOne + intervalOne
        relNoteThree = relNoteTwo + intervalTwo
        lowest = min([relNoteOne, relNoteTwo, relNoteThree])
        highest = max([relNoteOne, relNoteTwo, relNoteThree])
        noteRange = highest - lowest
        lowNote = random.randint(lowerMidiLimit, upperMidiLimit - noteRange)
        self.absNoteOne = lowNote + (lowest * -1)
        self.absNoteTwo = self.absNoteOne + intervalOne
        self.absNoteThree = self.absNoteTwo + intervalTwo

        #randomly choose note duration
        self.noteDur = random.uniform(self.minNoteDur, self.maxNoteDur)

        #set answer values
        self.intervalOneAnswer = kissearutil.midiToDiatonic(abs(intervalOne))
        self.intervalTwoAnswer = kissearutil.midiToDiatonic(abs(intervalTwo))

    def playNotes(self, port):
        #create messages
        msgOne = Message('note_on', note=self.absNoteOne, velocity=127)
        msgTwo = Message('note_on', note=self.absNoteTwo, velocity=127)
        msgThree = Message('note_on', note=self.absNoteThree, velocity=127)

        #play notes
        port.send(msgOne)
        time.sleep(self.noteDur)
        port.send(Message('note_off', note=self.absNoteOne))

        port.send(msgTwo)
        time.sleep(self.noteDur)
        port.send(Message('note_off', note=self.absNoteTwo))

        port.send(msgThree)
        time.sleep(self.noteDur)
        port.send(Message('note_off', note=self.absNoteThree))

    def checkAnswer(self, responses):
        if len(responses) != 2:
            print('Invalid entry.')
        else:
            intervalOneResponse = responses[0]
            intervalTwoResponse = responses[1]
            if intervalOneResponse != self.intervalOneAnswer or intervalTwoResponse != self.intervalTwoAnswer:
                print('Incorrect.')
            else:
                print('Correct!')
