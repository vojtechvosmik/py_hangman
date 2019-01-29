# coding=utf-8
import random

totalWins = 0
totalLoses = 0


class Difficulty:  # difficulty enum class
    EASY = 1
    HARD = 2
    EASY_ALLOWED_ATTEMPTS = 7
    HARD_ALLOWED_ATTEMPTS = 5


class HangMan:  # main hangman class
    wrongAttempts = 0
    allLettersGuessed = False

    @staticmethod
    def choose_difficulty():  # prints difficulty question and validates answer
        try:
            difficulty = str(raw_input("Choose difficulty(easy, hard) -> "))
            if difficulty == "easy":
                return Difficulty.EASY
            elif difficulty == "hard":
                return Difficulty.HARD
            else:
                return None
        except ValueError:
            return None

    @staticmethod
    def get_word_list(difficulty):  # gets word list from txt based on difficulty
        file_name = ""
        if difficulty == Difficulty.EASY:
            file_name = "easy"
        elif difficulty == Difficulty.HARD:
            file_name = "hard"
        else:
            return None
        with open("word_lists/" + file_name + ".txt", "r") as f:
            word_list = [line.strip() for line in f]
            return word_list

    @staticmethod
    def get_attempt(): #TODO check number
        try:
            attempt = str(raw_input("Guess letter -> "))
            if len(attempt) == 1:
                return attempt
            else:
                return None
        except ValueError:
            return None

    @staticmethod
    def check_attempt(attempt, word):  # checks if attempt is right or not
        if attempt in word:
            return True
        else:
            HangMan.wrongAttempts = HangMan.wrongAttempts + 1
            return False

    @staticmethod
    def ask_play_again():  # prints play again question at the end
        try:
            playAgain = str(raw_input("Wanna try again?(y, n) -> "))
            if playAgain == "y":
                HangMan.start()
            elif playAgain == "n":
                print("Poor..")
                exit()
            else:
                print("y or n expected")
                HangMan.ask_play_again()
        except ValueError:
            print "y or n expected"
            HangMan.ask_play_again()

    @staticmethod
    def print_total_score():  # prints proc. score
        global totalWins
        global totalLoses
        totalAttempts = totalWins + totalLoses
        winsProc = (100 * totalWins) / totalAttempts
        losesProc = 100 - winsProc
        print("Wins: " + str(winsProc) + "% loses: " + str(losesProc) + "%")

    @staticmethod
    def pretty_print_progress(guessed_letters, word):  # prints word progress
        pretty_progress = ""
        for letter in word:
            guessed = False
            for right_attempt in guessed_letters:
                if letter == right_attempt:
                    guessed = True
            if guessed:
                pretty_progress = pretty_progress + " " + letter
            else:
                pretty_progress = pretty_progress + " _"
        print('\x1b[0;30;44m' + pretty_progress + '\x1b[0m')

    @staticmethod
    def start():  # starts the game
        global totalWins
        global totalLoses
        HangMan.wrongAttempts = 0

        selected_difficulty = HangMan.choose_difficulty()
        if selected_difficulty is None:
            print("Easy or hard expected")
            HangMan.start()
        word_list = HangMan.get_word_list(selected_difficulty)
        if selected_difficulty is None:
            print("Something happened on the way to heaven.. please try it again :)")
            HangMan.start()

        full_word = random.choice(word_list)
        # print(full_word)  # cheat :P
        word = full_word
        guessed_letters = []
        allowed_wrong_attempts = Difficulty.EASY_ALLOWED_ATTEMPTS
        if selected_difficulty == Difficulty.HARD:
            allowed_wrong_attempts = Difficulty.HARD_ALLOWED_ATTEMPTS

        while not HangMan.allLettersGuessed:
            if HangMan.wrongAttempts > allowed_wrong_attempts:
                print("You lost..")
                print("The right word was: " + full_word)
                totalLoses = totalLoses + 1
                HangMan.print_total_score()  # TODO
                HangMan.ask_play_again()
            if len(word) == 0:
                print("You won..")
                totalWins = totalWins + 1
                HangMan.print_total_score()
                HangMan.ask_play_again()

            attempt = HangMan.get_attempt()
            if attempt is not None:
                if HangMan.check_attempt(attempt, word):
                    word = word.replace(attempt, "")
                    guessed_letters.append(attempt)
                    print('\x1b[6;30;42m' + 'Nice one!' + '\x1b[0m')
                    HangMan.pretty_print_progress(guessed_letters, full_word)
                else:
                    print('\x1b[5;30;41m' + 'Nope..' + '\x1b[0m')
                lives = allowed_wrong_attempts - HangMan.wrongAttempts
                if lives > 0:
                    print('\x1b[0;30;44m' + "♡ " + str(lives) + "/" + str(allowed_wrong_attempts) + '\x1b[0m')
            else:
                print("One letter without special chars expected!")


HangMan.start()
