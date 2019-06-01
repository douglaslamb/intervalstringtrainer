def diatonicToMidi(diatonicString):
    diatonicStringArr = ['m2', 'M2', 'm3', 'M3', 'P4', 'TT', 'P5', 'm6', 'M6', 'm7', 'M7', 'P8']
    midiInterval = diatonicStringArr.index(diatonicString) + 1
    return midiInterval
