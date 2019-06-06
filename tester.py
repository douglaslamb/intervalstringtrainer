import time

class Tester:
    # runs tests with multiple questions

    def __init__(self, player):
        self.player = player
        # default values
        self.numQuestions = 10 
        self.numPlays = 3
        self.speed= 1
        self.repeatDelta = 3 
        self.nextQuestionDelta = 4
        self.answerStrings = []
        
        try:
            numQuestions = int(raw_input('Enter number of questions.\n'))
        except ValueError:
            pass
        else:
            if numQuestions > 0:
                self.numQuestions = numQuestions

        try:
            numPlays = int(raw_input('Enter number of times to play each question.\n'))
        except ValueError:
            pass
        else:
            if numPlays > 0:
                self.numPlays = numPlays

        try:
            speed = int(raw_input('Enter speed. Default: 1.\n'))
        except ValueError:
            pass
        else:
            if speed > 0:
                self.speed = speed

        print('Questions: ' + str(self.numQuestions))
        print('Plays per question: ' + str(self.numPlays))
        print('Speed: ' + str(self.speed))
        print('\n')

    def run(self):
        for i in range(self.numQuestions):
            thisAnswers = self.player.chooseNotes()
            self.answerStrings.append(self.player.chooseNotes())
            for j in range(self.numPlays):
                self.player.playNotes()
                time.sleep(self.repeatDelta * self.speed)
            time.sleep(self.nextQuestionDelta * self.speed)
        print('Answers:')
        for i, answer in enumerate(self.answerStrings):
            printStr = str(i + 1) + '. '
            for item in answer:
                printStr = printStr + item + ' '
            print(printStr)
