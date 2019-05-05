# CLI Ear Trainer - an ear training program for the command line
# Copyright (C) 2019 Douglas Lamb 
# douglaslamb@douglaslamb.com

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# 
import mido
from mido import Message
import random
import time
import stringTrainer
import chordTrainer
import intervalTrainer

# globals
lowerMidiLimit = 36
upperMidiLimit = 96
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
    activityNumber = raw_input('Choose activity:\n1. Interval String Identification\n2. Chord Identification\n3. Interval Identification\n')

    # assign program module depending on user input
    if activityNumber == `1`:
        trainer = stringTrainer.StringTrainer()
    elif activityNumber == `2`:
        trainer = chordTrainer.ChordTrainer()
    elif activityNumber == `3`:
        trainer = intervalTrainer.IntervalTrainer()
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

        rawAnswer = raw_input(trainer.promptText + ' blank - repeat, n - next question, q - quit: ')

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
