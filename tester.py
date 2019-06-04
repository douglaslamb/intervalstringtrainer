class Tester:

    def __init__(self, generator):
        self.generator = generator
        # default values
        self.numQuestions = 10 
        self.numRepeats = 3
        self.speed= 1
        self.answerStrings = []
        
        try:
            numQuestions = int(raw_input('Enter number of questions.\n'))
        except ValueError:
            pass
        else:
            self.numQuestions = numQuestions

        try:
            numRepeats = int(raw_input('Enter number of repeats per question.\n'))
        except ValueError:
            pass
        else:
            self.numRepeats = numRepeats

        try:
            speed = int(raw_input('Enter speed. Default: 1.\n'))
        except ValueError:
            pass
        else:
            self.speed = speed



