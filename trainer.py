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
outPort = None

# prompt to choose midi port
while outPort == None:
    midiPorts = mido.get_output_names()
    midiPortsString = ''
    for i, port in enumerate(midiPorts):
        midiPortsString = midiPortsString + str(i + 1) + '. ' + port + '\n'
    try:
        portSelection = int(raw_input('Choose midi out port:\n' + midiPortsString))
    except ValueError:
        print('Invalid entry.\n')
        continue
    if portSelection < 1 or portSelection > len(midiPorts):
        print('Invalid entry.\n')
        continue
    outPort = mido.open_output(midiPorts[portSelection - 1])
    print('Using ' + outPort.name + ' for midi output.\n')

quit = False
trainer = None

# Start Menu
while trainer == None:
    activityNumber = raw_input('Choose activity:\n1. Interval String Identification\n2. Chord Identification\n')

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

        rawAnswer = raw_input(trainer.promptText + ' blank - repeat, n - next string, q - quit: ')

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
