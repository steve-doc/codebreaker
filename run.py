import gspread
from random import randrange
from os import system
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

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
    def show(self):
        print(f"Attempt: {self.attempt} Hit: {self.hit}  Miss: {self.miss}")

def welcome_banner():
    """
    Prints welcome screen to console after clearing screen.
    """
    system('clear')
    print("\n", "Welcome to\n", """  ______          __        ____                  __             __
  / ____/___  ____/ /__     / __ )________  ____ _/ /_____  _____/ /
 / /   / __ \/ __  / _ \   / __  / ___/ _ \/ __ `/ //_/ _ \/ ___/ / 
/ /___/ /_/ / /_/ /  __/  / /_/ / /  /  __/ /_/ / ,< /  __/ /  /_/  
\____/\____/\__,_/\___/  /_____/_/   \___/\__,_/_/|_|\___/_/  (_)   \n\n""")
    print("A 'Hit' means you have guessed the RIGHT number in the RIGHT place\n")
    print("A 'Miss' means you have guessed the RIGHT number in the WRONG place\n")




def generate_code(code_length):
    """
    Generate randon code of 3, 4 or 5 characters in length
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

def get_player_guess():
    """
    Ask for user guess and check it is intiger andcorrect length
    """
    while True:
        try:
            guess = 0
            while len(str(guess)) != 4:
                guess = int(input("\nEnter a 4 digit number to crack the code: "))
                if len(str(guess)) != 4:
                    print("Must be 4 digits long")

            break
        except ValueError:
            print("must be an Integer")
    return guess

def make_list(data):
    """
    Convert code or guess into a list for easier comparison.
    Passed a number, converts to string and then to list.
    Returns list
    """
    this_list = []
    string = str(data)
    this_list = [char for char in string]
    return this_list

def check_answer(code, guess):
    """
    Checks each character of code for exact match then for 
    near misses (right character in wrong place).
    Buils lists of matches and near misses.
    Returns length of each list.
    """
    code_list = make_list(code)
    guess_list = make_list(guess)
    remain_code_list = code_list
    remain_guess_list = guess_list
    match_list = []

    if guess == code:
        print("Well done, you broke the code!")
        exact_match = len(code_list)
        near_miss = 0
    else:
        for i in range(len(code_list) -1, -1, -1):
            # print(i)
            # print(code_list[i], guess_list[i])
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
    """
    alist.append(attempt)
    return alist

def show_previous_attempts(attempt_list):
    """
    First clear screen and reprint welcome banner
    Print list of attempts and results to screen
    before next attempt.
    """
    welcome_banner()

    print("The secret code is\n")
    print("X X X X\n")

    if len(attempt_list) != 0:
        for att in attempt_list:
            x = attempt_list.index(att) + 1
            print(f"Attempt {x:02d}: {att.attempt}      Hit: {att.hit} Near Miss: {att.miss}")
            # print(att.show()) 

def game_over():
    print("GAME OVER!!!")

def get_player_name():
    user = input("Please enter a new or existing user name: ")
    return user

def check_existing_player(user):
    players = SHEET.get_all_values()
    for player in players:
        if user == player[0]:
            print(f"Welcome back {user}, are you ready to beat your previous score?")
            return
    
    print(f"Welcome to CodeBreak {user}, would you like to see the rules?")
    new_user = [user, "none", "none", "none"]
    SHEET.append_row(new_user)

def main():
    """
    Main game function
    """
    code = generate_code(4)
    attempt_list = []
    exact_match = 0
    while exact_match != len(str(code)):
        if attempt_list != "done":
            show_previous_attempts(attempt_list)
            guess = get_player_guess()
            exact_match, near_miss = check_answer(code, guess)
            current_attempt = Attempt(guess, exact_match, near_miss)
            attempt_list = build_attempt_list(attempt_list, current_attempt)

    game_over()

welcome_banner()

# main()

player = get_player_name()
check_existing_player(player)






