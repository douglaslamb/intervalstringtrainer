import mido
from mido import Message
import random
import time


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
        self.intervalsArr = ['m2', 'M2', 'm3', 'M3', 'P4', 'TT', 'P5', 'm6', 'M6', 'm7', 'M7', 'P8']
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
        # check this line below, not sure if lowest * -1 is necessary
        self.absNoteOne = lowNote + (lowest * -1)
        self.absNoteTwo = self.absNoteOne + intervalOne
        self.absNoteThree = self.absNoteTwo + intervalTwo

        #randomly choose note duration
        self.noteDur = random.uniform(self.minNoteDur, self.maxNoteDur)

        #set answer values

        self.intervalOneAnswer = self.intervalsArr[abs(intervalOne) - 1]
        self.intervalTwoAnswer = self.intervalsArr[abs(intervalTwo) - 1]
        #print(intervalOneAnswer)
        #print(intervalTwoAnswer)

    #playNotes = True
    #done = False

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
            #print(intervalOneResponse)
            intervalTwoResponse = responses[1]
            #print(responses)
            if intervalOneResponse != self.intervalOneAnswer or intervalTwoResponse != self.intervalTwoAnswer:
                print('Incorrect.')
            else:
                print('Correct!')

#        print([intervalOne, intervalTwo])
#        print([relNoteOne, relNoteTwo, relNoteThree])
#        print([absNoteOne, absNoteTwo, absNoteThree])
