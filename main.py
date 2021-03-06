# kissear - an ear training program for the command line
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
import stringPlayer
import chordPlayer
import intervalPlayer
import trainer
import tester

# globals
# default midi limits
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

# prompt to choose midi range
midiLimitsInputRaw = raw_input('Set midi note range. Enter both limits (inclusive) as integers, separated by a space. Must have at least two-octave range.\nDefault: ' + str(lowerMidiLimit) + ' ' + str(upperMidiLimit) + '\n')
midiLimitsInput = midiLimitsInputRaw.split(' ')
necMidiRange = 24
midiSpecMin = 21
midiSpecMax = 108

if len(midiLimitsInput) == 2:
    # check if input strings are integers
    try:
        lowerMidiLimitInput = int(midiLimitsInput[0])
        upperMidiLimitInput = int(midiLimitsInput[1])
    except ValueError:
        print('Invalid input.')
    else:
        # check if input integers are appropriate midi notes
        if lowerMidiLimitInput >= midiSpecMin and lowerMidiLimitInput <= midiSpecMax and upperMidiLimitInput >= midiSpecMin and upperMidiLimitInput <= midiSpecMax and upperMidiLimitInput - lowerMidiLimitInput >= necMidiRange:
            lowerMidiLimit = lowerMidiLimitInput
            upperMidiLimit = upperMidiLimitInput
        else:
            print('Invalid input.')
else:
    print('Invalid input.')

print('Midi range is ' + str(lowerMidiLimit) + ' - ' + str(upperMidiLimit) + '.\n')

# Start Menu
playerClass = None
while playerClass == None:
    activityNumber = raw_input('Choose thing to work on:\n1. String Identification\n2. Chord Identification\n3. Interval Identification\n')

    # assign player depending on user input
    if activityNumber == `1`:
        playerClass = stringPlayer.StringPlayer
    elif activityNumber == `2`:
        playerClass = chordPlayer.ChordPlayer
    elif activityNumber == `3`:
        playerClass = intervalPlayer.IntervalPlayer
    else:
        print('Invalid entry.')

administratorClass = None
while administratorClass == None:
    activityNumber = raw_input('Choose format:\n1. Individual questions with immmediate answer prompt\n2. Multiple question quiz with answers displayed at end\n')

    # assign administrator depending on user input
    if activityNumber == `1`:
        administratorClass = trainer.Trainer
    elif activityNumber == `2`:
        administratorClass = tester.Tester
    else:
        print('Invalid entry.')

administrator = administratorClass(playerClass(lowerMidiLimit, upperMidiLimit, outPort))
administrator.run()
