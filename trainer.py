import kissearutil

class Trainer:
    # manages high level aspects of posing questions
    # with immediate user answer

    def __init__(self, player):
        self.player = player

    def run(self):
        quit = False
        while not quit:
            correctAnswer = self.player.chooseNotes()

            playNotes = True
            done = False

            # question loop
            while not done:
                if playNotes:
                    self.player.playNotes()
                    playNotes = False

                rawAnswer = raw_input(self.player.promptText + ' blank - repeat, n - next question, q - quit: ')

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
                    if len(responses) != len(correctAnswer):
                        print('Invalid entry.')
                    else:
                        for i, item in enumerate(responses):
                            if item == correctAnswer[i]:
                                print('Correct!')
                            else:
                                print('Incorrect.')
