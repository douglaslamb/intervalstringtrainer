import mido
from mido import Message
import random
import time
import csv
import os
import kissearutil

class ChordPlayer:

    def __init__(self, lowerMidiLimit, upperMidiLimit, outPort):
        self.lowerMidiLimit = lowerMidiLimit
        self.upperMidiLimit = upperMidiLimit
        self.outPort = outPort
        self.minDur = 1 
        self.maxDur = 3 
        self.dur = None
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

    def chooseNotes(self):
        # randomly choose and save a chord from the arr
        self.currChord = random.choice(self.chordsArr)
        chordIntervals = self.currChord[1]
        # get the range
        intervalRange = 0
        for interval in chordIntervals:
            intervalRange += interval

        # randomly choose and save the low note
        self.currLowNote = random.randint(self.lowerMidiLimit, self.upperMidiLimit - intervalRange)

        # randomly choose duration
        self.dur = random.uniform(self.minDur, self.maxDur)

        # return answer string in arr
        answerString = self.currChord[0]
        return [answerString]

    def playNotes(self):
        # generate midi note values
        midiNotes = [self.currLowNote]
        chordIntervals = self.currChord[1]
        for i, interval in enumerate(chordIntervals):
            newNote = midiNotes[i] + interval
            midiNotes.append(newNote)

        # play notes
        for midiNote in midiNotes:
            self.outPort.send(Message('note_on', note=midiNote, velocity=127))

        time.sleep(self.dur)

        # end notes
        for midiNote in midiNotes:
            self.outPort.send(Message('note_off', note=midiNote))
