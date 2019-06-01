diatonicStrings = ['m2', 'M2', 'm3', 'M3', 'P4', 'TT', 'P5', 'm6', 'M6', 'm7', 'M7', 'P8']

def diatonicToMidi(diatonicString):
    midiInterval = diatonicStrings.index(diatonicString) + 1
    return midiInterval

def midiToDiatonic(midiInterval):
    diatonicString = diatonicStrings[midiInterval - 1]
    return diatonicString
