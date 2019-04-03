import mido
from mido import Message
import random
import time
import stringTrainer
##import chordTrainer

# globals
lowerMidiLimit = 36
upperMidiLimit = 96
intervalsArr = ['m2', 'M2', 'm3', 'M3', 'P4', 'TT', 'P5', 'm6', 'M6', 'm7', 'M7', 'P8']

# prompt to choose midi port
print(mido.get_output_names())
portName = input('Enter name of midi out port including single quotes:')
outPort = mido.open_output(portName)
quit = False
trainer = None

# Start Menu
while trainer == None:
    activityNumber = raw_input('''Choose activity:
            1. Interval String Identification
            2. Chord Identification\n''')

    # assign program module depending on user input
    if activityNumber == `1`:
        trainer = stringTrainer.StringTrainer()
    elif activityNumber == `2`:
        #trainer = chordTrainer.chordTrainer
        print('nothing here yet')
    else:
        print('Invalid entry.')

# main loop
while not quit:
    trainer.chooseNotes(lowerMidiLimit, upperMidiLimit)

    playNotes = True
    done = False

    # question loop
    while not done:
        if playNotes:
            trainer.playNotes(outPort)
            playNotes = False

        rawAnswer = raw_input(trainer.promptText + 'blank - repeat, n - next string, q - quit: ')

        # check answers
        if rawAnswer == '':
            playNotes = True
        elif rawAnswer == 'n':
            done = True
        elif rawAnswer == 'q':
            done = True
            quit = True
        else:
            responses = rawAnswer.split(' ')
            trainer.checkAnswer(responses)

#        print([intervalOne, intervalTwo])
#        print([relNoteOne, relNoteTwo, relNoteThree])
#        print([absNoteOne, absNoteTwo, absNoteThree])
