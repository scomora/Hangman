import stdiomask
from os import system
from random import randint

masks = ['*', '?', '-', '.', '+', '$', '@']

hangmanGraphics = [
    # 0 incorrect guesses
    """
     +--+
     |  |
        |
        |
        |
        |
        |
    ----+----
    """,
    """
     +--+
     |  |
     O  |
        |
        |
        |
        |
    ----+----
    """,
    """
     +--+
     |  |
     O  |
     |  |
     |  |
        |
        |
    ----+----
    """,
    """
     +--+
     |  |
     O  |
     |/ |
     |  |
        |
        |
    ----+----
    """,
    """
     +--+
     |  |
     O  |
    \|/ |
     |  |
        |
        |
    ----+----
    """,
    """
     +--+
     |  |
     O  |
    \|/ |
     |  |
      \ |
        |
    ----+----
    """,
    """
     +--+
     |  |
     O  |
    \|/ |
     |  |
    / \ |
        |
    ----+----
    """
]


def anyDigits(s):
    return any(char.isdigit() for char in s)


def processWordInput():
    while True:
        wordIn = stdiomask.getpass(
            prompt="Enter a word: ",
            mask=masks[randint(0, len(masks) - 1)]
        )
        if wordIn is None or len(wordIn) == 0 or wordIn.isspace():
            print("-ERR: you failed to enter a word!")
            continue
        elif anyDigits(wordIn):
            print("-ERR: you entered a number!")
            continue
        elif not wordIn.isalpha():
            print("-ERR: you entered a non-letter!")
            continue
        else:
            print("I got your word. Don't worry - I won't reveal it!")
            return wordIn



def processLetterInput(prompt):
    while True:
        letterGuess = input(prompt)
        if letterGuess is None or len(letterGuess) == 0:
            print("-ERR: you failed to enter a letter!")
            continue
        else:
            return letterGuess


class Hangman:
    def __init__(self, wordToGuess):
        """
        wordToGuess =   foxes
        currGuessed =   _o_e_
        :param wordToGuess:
        """
        self.wordToGuess = wordToGuess
        self.numOfGuesses = 0
        self.numIncorrectGuesses = 0
        self.currGuessedWord = []
        self.lastLetterGuessedCorrectly = False
        self.initCurrGuessedWord()

        self.incorrectGuessedLetters = []
        self.gameWon = False
        self.gameOver = False
        self.printBoard()

    def initCurrGuessedWord(self):
        for char in self.wordToGuess:
            self.currGuessedWord.append(' ')

    def printBoard(self):
        self.printCurrGuessedWord()
        self.printDashes()

    def printCurrGuessedWord(self):
        ret = ""
        for guessedChar in self.currGuessedWord:
            ret += "{} ".format(guessedChar)
        return ret

    def printDashes(self):
        dashes = ""
        for i in range(len(self.wordToGuess)):
            dashes += "- "
        return dashes

    def gameWasWon(self):
        self.gameOver = True
        self.gameWon = True

    def processGuess(self, guessInput):
        if isinstance(guessInput, WordGuess):
            self.processWordGuess(guessInput)
        elif isinstance(guessInput, LetterGuess):
            self.processLetterGuess(guessInput)

    def processWordGuess(self, guessedWord):
        assert (guessedWord.correct is False)
        assert ((self.gameWon or self.gameOver) is False)
        if guessedWord.guess == self.wordToGuess:
            guessedWord.correct = True
            self.gameOver = True
            self.gameWon = True
        else:
            guessedWord.sizeDifferenceFromWordToGuess = len(guessedWord.guess) - len(self.wordToGuess)

    def processLetterGuess(self, guessedLetter):
        if guessedLetter.guess in (self.currGuessedWord + self.incorrectGuessedLetters):
            guessedLetter.wasAlreadyGuessed = True
            return
        else:
            # if word was entered for some reason
            if len(guessedLetter.guess) > 1:
                return
            if guessedLetter.guess in self.wordToGuess:
                self.lastLetterGuessedCorrectly = True
                charIdx = 0
                numInstances = 0
                gameWon = True
                for charIdx in range(len(self.wordToGuess)):
                    if self.wordToGuess[charIdx] == guessedLetter.guess:
                        self.currGuessedWord[charIdx] = guessedLetter.guess
                        numInstances += 1
                    if self.currGuessedWord[charIdx] != self.wordToGuess[charIdx]:
                        gameWon = False
                    charIdx += 1
                self.gameWon = gameWon
                self.gameOver = self.gameWon
                guessedLetter.numOccurences = numInstances
            else:  # wrong guess!
                self.incorrectGuessedLetters.append(guessedLetter.guess)
                self.incrementNumIncorrectGuesses()
                if self.numIncorrectGuesses >= 6:
                    self.gameOver = True
                    assert (self.gameWon is False)
            self.incrementNumberOfGuesses()
        return

    def incrementNumIncorrectGuesses(self):
        self.numIncorrectGuesses += 1

    def incrementNumberOfGuesses(self):
        self.numOfGuesses += 1

    def __str__(self):
        # print the hangman graphic
        retVal = hangmanGraphics[self.numIncorrectGuesses]
        # print the currently guessed word
        retVal += "\n" + self.printCurrGuessedWord()
        retVal += "\n" + self.printDashes()
        retVal += "\n" + "Number of guesses remaining: {}".format(str(6 - self.numIncorrectGuesses))
        retVal += "\n" + "Letters already guessed: {}".format(str(self.incorrectGuessedLetters))
        return retVal


class Gallow:
    head = 'o'
    body = '||'
    leftArm = '-'
    rightArm = '-'
    leftLeg = '/'
    rightLeg = '\\'
    maxNumMistakes = 6

    def __init__(self):
        self.numMistakes = 0

    def __str__(self):
        """
        @TODO implement
        :return:
        """
        pass
        # retVal = gallow
        if self.numMistakes == 0:
            return ""
        elif self.numMistakes == 1:
            return


class Guess:
    def __init__(self, guess):
        self.guess = guess
        self.correct = False


class WordGuess(Guess):
    def __init__(self, guessedWord):
        super().__init__(guessedWord)
        self.sizeDifferenceFromWordToGuess = 0

    def printIncorrectGuess(self):
        print("{} is not ".format(self.guess))


class LetterGuess(Guess):
    def __init__(self, guessedLetter):
        super().__init__(guessedLetter)
        self.numOccurences = 0
        self.wasAlreadyGuessed = True

    def incrementNumOccurences(self):
        self.numOccurences += 1

    def printIncorrectGuess(self):
        print("{} is not the word I'm looking for!".format(self.guess))


def driver():
    while True:
        system('clear')
        print("Welcome to hangman!")
        hangman = Hangman(processWordInput())
        print(hangman)
        currGuess = object()
        while not hangman.gameOver:
            letterOrWordGuessInput = processLetterInput("Enter a letter to guess or -wg to "
                                                        "guess a complete word/phrase: ")
            if letterOrWordGuessInput == "--wordguess" or letterOrWordGuessInput == "-wg":
                wordGuess = processWordInput()
                currGuess = WordGuess(wordGuess)
            else:
                currGuess = LetterGuess(letterOrWordGuessInput)
            hangman.processGuess(currGuess)
            # clear terminal
            system('clear')
            print(hangman)
            print("")
        if hangman.gameWon:
            print("You won!")
        else:
            print("You lost :(")
        print("\nThe word was *** {} ***".format(hangman.wordToGuess.upper()))
        wantToPlayAgain = processLetterInput(("Would you like to play again? [y/n]: "))
        if wantToPlayAgain.lower() == 'n':
            break


if __name__ == '__main__':
    driver()
