import mido
from mido import Message
import random
import time
import csv
import os
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
        self.userMidiIntervals = []

        intervalsFile = os.path.expanduser(raw_input('Enter path of intervals csv file.\n'))
        # csv import currently does no checks for invalid input
        # the first and only row must be comma separated interval strings (e.g., P5) with no whitespace
        with open(intervalsFile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            userIntervalStrings = csv_reader.next()
            for item in userIntervalStrings:
                self.userMidiIntervals.append(kissearutil.diatonicToMidi(item))

    def chooseNotes(self):
        #randomly choose intervals and notes
        intervalOne = random.choice(self.userMidiIntervals) * random.choice([-1, 1])
        intervalTwo = random.choice(self.userMidiIntervals) * random.choice([-1, 1])
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
        self.outPort.send(msgOne)
        time.sleep(self.noteDur)
        self.outPort.send(Message('note_off', note=self.absNoteOne))

        self.outPort.send(msgTwo)
        time.sleep(self.noteDur)
        self.outPort.send(Message('note_off', note=self.absNoteTwo))

        self.outPort.send(msgThree)
        time.sleep(self.noteDur)
        self.outPort.send(Message('note_off', note=self.absNoteThree))
