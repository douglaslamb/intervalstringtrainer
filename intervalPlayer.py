import mido
from mido import Message
import random
import time
import csv
import os
import kissearutil

class IntervalPlayer:

    def __init__(self, lowerMidiLimit, upperMidiLimit, outPort):
        self.lowerMidiLimit = lowerMidiLimit
        self.upperMidiLimit = upperMidiLimit
        self.outPort = outPort
        self.minDur = 0.5
        self.maxDur = 1.2
        self.dur = None
        self.promptText = "Enter interval."

        self.userMidiIntervals = []
        self.playFuncs = []

        self.currMidiInterval = None
        self.currMidiNotes = []
        self.currPlayFunc = None
        self.currLowNote = None

        intervalsFile = os.path.expanduser(raw_input('Enter path of intervals csv file.\n'))
        # csv import currently does no checks for invalid input
        # the first and only row must be comma separated interval strings (e.g., P5) with no whitespace
        with open(intervalsFile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            userIntervalStrings = csv_reader.next()
            for item in userIntervalStrings:
                self.userMidiIntervals.append(kissearutil.diatonicToMidi(item))

        #print(self.userMidiIntervals)

        isPlayUp = raw_input('Intervals played up? y/n\n')
        isPlayDown = raw_input('Intervals played down? y/n\n')
        isPlayHarmonic = raw_input('Intervals played harmonically? y/n\n')

        if isPlayUp == 'y':
            self.playFuncs.append(self.playUp)
        if isPlayDown == 'y':
            self.playFuncs.append(self.playDown)
        if isPlayHarmonic == 'y':
            self.playFuncs.append(self.playHarmonic)

    def chooseNotes(self):
        # randomly choose an interval and playfunc
        self.currMidiInterval = random.choice(self.userMidiIntervals)
        self.currPlayFunc = random.choice(self.playFuncs)

        # randomly choose the low note
        self.currLowNote = random.randint(self.lowerMidiLimit, self.upperMidiLimit - self.currMidiInterval)

        # randomly choose duration
        self.dur = random.uniform(self.minDur, self.maxDur)

        # return answer string in arr
        return [kissearutil.midiToDiatonic(abs(self.currMidiInterval))]

    def playNotes(self):
        self.currPlayFunc(self.currLowNote, self.currMidiInterval, self.outPort)

    def playUp(self, lowNote, interval, port):
        highNote = lowNote + interval
        self.playSequential(lowNote, highNote, port)

    def playDown(self, lowNote, interval, port):
        highNote = lowNote + interval
        self.playSequential(highNote, lowNote, port)

    def playSequential(self, noteOne, noteTwo, port):
        #create messages
        msgOne = Message('note_on', note=noteOne, velocity=127)
        msgTwo = Message('note_on', note=noteTwo, velocity=127)

        #play notes
        port.send(msgOne)
        time.sleep(self.dur)
        port.send(Message('note_off', note=noteOne))

        port.send(msgTwo)
        time.sleep(self.dur)
        port.send(Message('note_off', note=noteTwo))

    def playHarmonic(self, lowNote, interval, port):
        # generate midi note values
        highNote = lowNote + interval

        # play notes
        port.send(Message('note_on', note=lowNote, velocity=127))
        port.send(Message('note_on', note=highNote, velocity=127))

        time.sleep(self.dur)

        # end notes
        port.send(Message('note_off', note=lowNote))
        port.send(Message('note_off', note=highNote))
