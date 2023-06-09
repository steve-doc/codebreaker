# Required Library imports
import gspread
from random import randrange
from os import system
import sys
from google.oauth2.service_account import Credentials

# Setup scope
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Setup credentials
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('code_breaker').sheet1


class Attempt:
    """
    A class to store code cracking attempts with results (hit, near miss)
    """
    def __init__(self, attempt, hit, miss):
        self.attempt = attempt
        self.hit = hit
        self.miss = miss

    def show(self, x):
        print(f"Attempt:{x:02d}",
              f"  \033[1;34m{self.attempt}\033[0m",
              f"   Hit: \033[0;32m{self.hit}\033[0m",
              f"  Near miss: \033[1;35m{self.miss}\033[0m")


def welcome_banner():
    """
    Prints welcome screen to console after clearing screen.
    """
    system('clear')
    print("\n", "Welcome to\n", """\033[34m
   ______          __        ____                  __             __
  / ____/___  ____/ /__     / __ )________  ____ _/ /_____  _____/ /
 / /   / __ \\/ __  / _ \\   / __  / ___/ _ \\/ __ `/ //_/ _ \\/ ___/ /
/ /___/ /_/ / /_/ /  __/  / /_/ / /  /  __/ /_/ / ,< /  __/ /  /_/
\\____/\\____/\\__,_/\\___/  /_____/_/   \\___/\\__,_/_/|_|\\___/_/  (_)
\033[0m \n\n""")


def game_menu(player):
    """
    Displays game menu, take user choice and acts on choice
    Argument:
        player - an array containing player name and
        best scores for each level.
    """

    choice = None
    while choice not in {"1", "2", "3", "4"}:
        welcome_banner()
        print("""
        1 - Play new game
        2 - Instructions
        3 - Leader Boards
        4 - Quit
        """)
        choice = input("Please choose: \n").strip()
        if choice == "1":
            main(player)
        elif choice == "2":
            instructions(player)
        elif choice == "3":
            high_scores(player)
        elif choice == "4":
            print("\n\nThanks for playing!\n")
            print("Please share Code Breaker with your friends",
                  "and come back soon!\n")
            update_spreadsheet(player)
            sys.exit(0)


def instructions(player):
    """
    Print out game instructions.
    Argument:
        player - an array containing player name and
        best scores for each level.
    """
    welcome_banner()

    print("""\033[31m
    ____           __                  __  _
   /  _/___  _____/ /________  _______/ /_(_)___  ____  _____
   / // __ \\/ ___/ __/ ___/ / / / ___/ __/ / __ \\/ __ \\/ ___/
 _/ // / / (__  ) /_/ /  / /_/ / /__/ /_/ / /_/ / / / (__  )
/___/_/ /_/____/\\__/_/   \\__,_/\\___/\\__/_/\\____/_/ /_/____/


        \033[0m""")
    print("""
The aim of the game is to crack the numeric code in as few attempts
as possible. So a low score is actually the Best Score.

The code will be either 3, 4, or 5 digits long, depending on the difficulty
of the game you choose (Easy, Normal or Difficult).

The codes will not have leading zeros, so nothing like 001 (easy)
or 01234 (normal).
Zeros can be used elsewhere in the code, so 101 (easy)
or 10000 (difficult) are valid.

3 digit codes are between 100 and 999
4 digit codes are between 1000 and 9999
5 digit codes are between 10000 and 99999
    """)
    choice = " "
    while choice != "":
        choice = input("\u001b[32mPress return to continue \033[0m\n")

    print("""
You will be asked to attempt a code.  Enter your attempt in the ranges above.

If you get the code exactly right you have won the game and your score will
be recorded if it is your first Score or your Best Score.

If you don't get the code exactly right you will be told how many "Hits"
or "Near Misses" your attempt achieved.

A "Hit" means you got a number right in the right position.

A "Near Miss" means you got a right number but in the wrong position.

The twist is you have to figure out which numbers we "Hits" and which
were "Near Misses"

As you progress you will see your previous attempts logged above so you
can use your logical skills to figure out the code.

GOOD LUCK WITH CRACKING THE CODE!\n
    """)

    choice = " "
    while choice != "":
        choice = input("\u001b[32mPress return to continue \033[0m\n")

    game_menu(player)


def high_scores(player):
    """
    displays three leaderboard for easy, normal & difficult levels.
    Argument:
        player - an array containing player name and
        best scores for each level.

    """
    players = SHEET.get_all_values()
    for ind, x in enumerate(players):
        if x[0] == player[0]:
            players[ind] = player

    # declares 3 empty lists
    easy = []
    normal = []
    difficult = []

    # Adds scores to each list where there is a score, not "None"
    for y in range(1, len(players)):
        if players[y][1] != "None":
            easy.append((players[y][0], players[y][1]))
        if players[y][2] != "None":
            normal.append((players[y][0], players[y][2]))
        if players[y][3] != "None":
            difficult.append((players[y][0], players[y][3]))

    # sorts lists based on score (second index of sub list)
    easy_sorted = sorted(easy, key=lambda x: int(x[1]))
    normal_sorted = sorted(normal, key=lambda x: int(x[1]))
    difficult_sorted = sorted(difficult, key=lambda x: int(x[1]))
    welcome_banner()

    # print 3 leaderboards with pause between each one
    print("EASY LEVEL LEADER BOARD\n")
    if len(easy_sorted) > 10:
        del easy_sorted[10:]
    for s in easy_sorted:
        print(f"{s[0]:15}  {s[1]}")

    choice = " "
    while choice != "":
        choice = input("\n\u001b[32mPress return to continue \033[0m\n")

    print("\n\nNORMAL LEVEL LEADER BOARD\n")
    if len(normal_sorted) > 10:
        del normal_sorted[10:]
    for s in normal_sorted:
        print(f"{s[0]:15}  {s[1]}")

    choice = " "
    while choice != "":
        choice = input("\n\u001b[32mPress return to continue \033[0m\n")

    print("\n\nDIFFICULT LEVEL LEADER BOARD\n")
    if len(difficult_sorted) > 10:
        del difficult_sorted[10:]
    for s in difficult_sorted:
        print(f"{s[0]:15}  {s[1]}")

    choice = " "
    while choice != "":
        choice = input("\n\u001b[32mPress return to continue \033[0m\n")

    game_menu(player)


def generate_code(code_length):
    """
    Generate random code of 3, 4 or 5 characters in length.
    Argument:
        code_length - an integer providing length of code
        to be generated.
    Returns:
        code - an integer that is code for game.
    """
    if code_length == 3:
        start = 100
        stop = 999
    elif code_length == 4:
        start = 1000
        stop = 9999
    else:
        start = 10000
        stop = 99999

    code = randrange(start, stop)

    return code


def get_player_guess(code_length):
    """
    Ask for user guess and check it is integer and correct length.
    Argument:
        code_length - an integer providing length of code
        to be generated.
    Return:
        guess = and integer input by player.
    """
    question = f"\nEnter a {code_length} digit" + \
               " number to crack the code (0 to quit): \n"
    while True:
        try:
            guess = 0
            while len(str(guess)) != code_length:

                guess = int(input(question))
                if guess == 0:  # If 0 exit game before finish
                    return guess
                guess = int(guess)
                if len(str(guess)) != code_length:
                    print(f"\nMust be {code_length} "
                          "digits long and not have leading zeros")

            break
        except ValueError:
            print("\nMust be an Integer")
    return guess


def make_list(data):
    """
    Convert code or guess into a list for easier comparison.
    Argument:
        data - an integer that is the latest guess from player.
    Returns:
        this_list - an array made up of each character from data argument
    """
    this_list = []
    string = str(data)
    this_list = [char for char in string]
    return this_list


def check_answer(code, guess):
    """
    Checks each character of code angainst the player's guess
    for exact match then for near misses (right character in wrong place).
    Builds lists of matches and near misses.
    Argument:
        code - an integer which is the code to be cracked.
        guess - an integeger which is the players current
        guess at the code.
    Returns:
        exact_match - integer with number of hits
        near_miss - integer with number of near misses
    """
    code_list = make_list(code)
    guess_list = make_list(guess)
    # declare copies of guess_list and code_list
    # these are decremented as the code checks the guess against
    # correct answer
    remain_code_list = code_list
    remain_guess_list = guess_list
    match_list = []
    if guess == code:
        exact_match = len(code_list)
        near_miss = 0
    else:
        for i in range(len(code_list) - 1, -1, -1):
            if guess_list[i] == code_list[i]:
                match_list.append(code_list[i])
                remain_code_list.pop(i)
                remain_guess_list.pop(i)
        exact_match = len(match_list)
        remain_matches = set(remain_code_list) & set(remain_guess_list)
        near_miss = len(remain_matches)

    return exact_match, near_miss


def build_attempt_list(alist, attempt):
    """
    add each attempt to the attempt_list so it can be printed
    out before the next attempt
    Argument:
        alist - an array in acculated list of previous guesses.
        attempt - integer with most recent guess from player.
    Returns:
        alist - updated list of attempts at code.
    """
    alist.append(attempt)
    return alist


def show_previous_attempts(attempt_list, code_length):
    """
    First clear screen and reprint welcome banner
    Print list of attempts and results to screen
    before next attempt.
    Argument:
        attempt_list - list of objects. Objects are previous attempts
        at code.
        code_length - an integer providing length of code
        to be generated.
    """
    welcome_banner()

    print("The secret code is\n")

    if code_length == 3:
        print("\033[0;31mX X X\033[0m\n")
    elif code_length == 4:
        print("\033[0;31mX X X X\033[0m\n")
    else:
        print("\033[0;31mX X X X X\033[0m\n")

    print("A 'Hit' means you have guessed the ",
          "RIGHT number in the RIGHT place\n")
    print("A 'Near Miss' means you have guessed the ",
          "RIGHT number in the WRONG place\n")

    if len(attempt_list) != 0:
        for att in attempt_list:
            x = attempt_list.index(att) + 1
            att.show(x)


def get_player_name():
    """
    Get player name.  Check it is alphanumeric.
    Returns :
        user - a string containing the name the player input.
    """
    user = "*"
    while not user.isalnum():
        user = input("Please enter a new or existing user name: \n")
        if not user.isalnum():
            print("Must be alphanumeric")
        else:
            return user


def check_existing_player(user):
    """
    Check if new or existing user.
    If existing show current Best Scores
    If new, add to spreadsheet with scores set to "None"
    Argument:
        user - a string containing the name the player input.
    Returns:
        player - an array containing player name and
        best scores for each level.
    """
    players = SHEET.get_all_values()
    for player in players:
        if user.lower() == player[0]:
            print("\nWelcome back", user,
                  ", are you ready to beat your current Best Scores?\n")
            print("You current Best Scores are\n")
            print(f"   Beginner - {player[1]}")
            print(f"   Normal - {player[2]}")
            print(f"   Difficult - {player[3]}\n")
            choice = " "
            while choice != "":
                choice = input("\u001b[32mPress return to continue \033[0m\n")
            return player

    print(f"\nWelcome to CodeBreaker {user}!\n")
    new_user = [user.lower(), "None", "None", "None"]
    SHEET.append_row(new_user)
    player = new_user
    choice = " "
    while choice != "":
        choice = input("\u001b[32mPress return to continue \033[0m\n")

    return player


def ask_game_level():
    """
    Takes input from player on what game level they want to play and
    returns level to be used for creating code length.
    Returns:
        level = a single character string with the chosen level.
    """
    print(" What level of game would you like to play?")
    print("\n(B)eginner (3 Digit code)")
    print("(N)ormal (4 Digit code)")
    print("(D)ifficult (5 Digit code)\n")
    check = True
    while check:
        lev = input("B/N/D: \n").strip()
        level = lev.lower()
        if level not in {"b", "n", "d"}:
            print("Must answer 'b', 'n' or 'd' ")
        else:
            check = False
    return level


def set_game_level(level):
    """
    sets code length based on game level
    Argument:
        level = a single character string with the chosen level.
    Returns:
        code_length = integer with length of code.
    """
    if level == "b":
        code_length = 3
    elif level == "d":
        code_length = 5
    else:
        code_length = 4

    return code_length


def game_over(input_name, attempt_number):
    """
    Display "Game Over" and tell player what their score was.
    Arguments:
        input_name - String with player name
        attempt_number - integer with the number of attempts it took to
        complete the game.
    """
    welcome_banner()
    print("GAME OVER!!!\n")
    print(f"Well done {input_name},",
          f" you broke the code in {attempt_number} attempts!\n")


def check_high_score(level, attempts, player):
    """
    Check if score beats existing high score.
    Arguments:
        level - string with game level.
        attempts - integer with number of attempts to complete game.
        player - an array containing player name and best scores for
        each level.
    Returns:
        player - an updated array containing player name and best scores
        for each level.
    """
    if level == "b":
        ind = 1
        level_name = "Beginner"
    elif level == "n":
        ind = 2
        level_name = "Normal"
    elif level == "d":
        ind = 3
        level_name = "Difficult"

    score = player[ind]

    # different message returned depending on how score compares
    # to previous Best Score
    if score == "None":
        print(f"Congratulations, you set your first Best Score",
              f" of {attempts} at {level_name} level\n")
        player[ind] = int(attempts)
    elif attempts < int(score):
        print(f"Congrats, you set a new Best Score of",
              f" {attempts} at {level_name} level\n")
        player[ind] = int(attempts)
    elif attempts == int(score):
        print(f"Not bad, you equalled your Best Score of",
              f" {attempts} at {level_name} level\n")
    else:
        print(f"Unfortunately, you missed your Best Score of",
              f" {player[ind]} by {attempts - int(score)} at ",
              f"{level_name} level\n")

    update_spreadsheet(player)

    choice = " "
    while choice != "":
        choice = input("\u001b[32mPress return to continue \033[0m\n")

    return player


def update_spreadsheet(player):
    """
    Update score on spreadsheet.
    Argument:
        player - an array containing player name and best scores for
        each level.
    """
    cell = SHEET.find(player[0])
    row = str(cell.row)
    update_range = "A" + row + ":" + "D" + row
    SHEET.update(update_range, [player])


def main(player):
    """
    Main game function
    Argument:
        player - an array containing player name and best scores for
        each level.
    Returns:
        Returns to game_menu function at end passing the updated player
        array.
    """
    welcome_banner()

    level = ask_game_level()
    code_length = set_game_level(level)
    code = generate_code(code_length)

    attempt_list = []
    exact_match = 0
    while exact_match != len(str(code)):
        show_previous_attempts(attempt_list, code_length)
        guess = get_player_guess(code_length)
        if guess == 0:
            game_menu(player)
        exact_match, near_miss = check_answer(code, guess)
        current_attempt = Attempt(guess, exact_match, near_miss)
        attempt_list = build_attempt_list(attempt_list, current_attempt)

    game_over(input_name, len(attempt_list))
    player = check_high_score(level, len(attempt_list), player)
    game_menu(player)


welcome_banner()
input_name = get_player_name()
player = check_existing_player(input_name)
game_menu(player)
