import mido
from mido import Message
import random
import time
import csv
import os

class ChordTrainer:

    def __init__(self):
        self.minDur = 0.5
        self.maxDur = 1.2
        self.noteDur = None
        self.currChord = None
        self.currLowNote = None
        self.correctAnswer = None
        self.chordsArr = [] 
        self.promptText = "Enter chord."
        chordFile = os.path.expanduser(raw_input('Enter path of chords csv file.\n'))
        #chords are stored as tuples in self.chordsarr as (answerString, [chord intervals])
        # csv import currently does no checks for invalid entries
        with open(chordFile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                chord = []
                for i, item in enumerate(row):
                    if i == 0:
                        answerString = item
                    else:
                        chord.append(int(item))
                self.chordsArr.append((answerString, chord))

    def chooseNotes(self, lowerMidiLimit, upperMidiLimit):
        # randomly choose and save a chord from the arr
        self.currChord = random.choice(self.chordsArr)
        chordIntervals = self.currChord[1]
        # get the range
        intervalRange = 0
        for interval in chordIntervals:
            intervalRange += interval

        # randomly choose and save a low note
        self.currLowNote = random.randint(lowerMidiLimit, upperMidiLimit - intervalRange)
        self.chordNotes[0] = lowNote

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
