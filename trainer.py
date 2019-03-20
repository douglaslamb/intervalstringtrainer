import mido
from mido import Message
import random
import time

lowerLimit = 36
upperLimit = 96

#prompt user to choose midi port
print(mido.get_output_names())
portName = input('type name of desired midi port including single quotes:')
outPort = mido.open_output(portName)

#randomly choose intervals and notes
intervalOne = random.randint(1, 12) * random.choice([-1, 1])
intervalTwo = random.randint(1, 12) * random.choice([-1, 1])
relNoteOne = 0
relNoteTwo = relNoteOne + intervalOne
relNoteThree = relNoteTwo + intervalTwo
lowest = min([relNoteOne, relNoteTwo, relNoteThree])
highest = max([relNoteOne, relNoteTwo, relNoteThree])
noteRange = highest - lowest
lowNote = random.randint(36, 96 - noteRange)
absNoteOne = lowNote + (lowest * -1)
absNoteTwo = absNoteOne + intervalOne
absNoteThree = absNoteTwo + intervalTwo

#create messages
msgOne = Message('note_on', note=absNoteOne, velocity=127)
msgTwo = Message('note_on', note=absNoteTwo, velocity=127)
msgThree = Message('note_on', note=absNoteThree, velocity=127)

#randomly choose note duration
noteDur = random.uniform(0.25, 1)

#play notes
outPort.send(msgOne)
time.sleep(noteDur)
outPort.send(Message('note_off', note=absNoteOne))

outPort.send(msgTwo)
time.sleep(noteDur)
outPort.send(Message('note_off', note=absNoteTwo))

outPort.send(msgThree)
time.sleep(noteDur)
outPort.send(Message('note_off', note=absNoteThree))

print([intervalOne, intervalTwo])
print([relNoteOne, relNoteTwo, relNoteThree])
print([absNoteOne, absNoteTwo, absNoteThree])
