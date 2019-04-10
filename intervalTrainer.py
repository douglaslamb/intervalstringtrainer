import mido
from mido import Message
import random
import time

class IntervalTrainer:

    def __init__(self):
        self.minNoteDur = 0.5
        self.maxNoteDur = 1.2
        self.noteDur = None
        self.isUpDownHarmonic = [False,False,False]
        self.intervalsArr = ['m2', 'M2', 'm3', 'M3', 'P4', 'TT', 'P5', 'm6', 'M6', 'm7', 'M7', 'P8']

        self.currMidiInterval = None
        self.currMidiNotes = []
        self.currPlayFunc = None
        self.promptText = "Enter interval:"

        self.userIntervals = []
        intervalsFile = os.path.expanduser(raw_input('Enter path of intervals csv file.\n'))
        # csv import currently does no checks for invalid input
        # the first and only row must be comma separated interval strings (e.g., P5) with no whitespace
        with open(intervalsFile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            self.userIntervals = csv_reader[0]

        print(userIntervals)

        upDownHarmonicResponses = []
        upDownHarmonicResponses[0] = raw_input('Intervals played up? y/n:')
        upDownHarmonicResponses[1] = raw_input('Intervals played down? y/n:')
        upDownHarmonicResponses[2] = raw_input('Intervals played harmonically? y/n:')

        for i, item in enumerate(upDownHarmonicResponses):
            if item == 'y':
                self.isUpDownHarmonic[i] = True

        print(upDownHarmonicResponses)
        print(isUpDownHarmonic)

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

        self.intervalOneAnswer = self.intervalsArr[abs(intervalOne) - 1]
        self.intervalTwoAnswer = self.intervalsArr[abs(intervalTwo) - 1]

    def playNotesSequential(self, port):
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
