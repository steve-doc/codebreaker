from random import randrange
from os import system


def welcome_banner():
    system('clear')
    print("\n", "Welcome to\n", """  ______          __        ____                  __             __
  / ____/___  ____/ /__     / __ )________  ____ _/ /_____  _____/ /
 / /   / __ \/ __  / _ \   / __  / ___/ _ \/ __ `/ //_/ _ \/ ___/ / 
/ /___/ /_/ / /_/ /  __/  / /_/ / /  /  __/ /_/ / ,< /  __/ /  /_/  
\____/\____/\__,_/\___/  /_____/_/   \___/\__,_/_/|_|\___/_/  (_)   """)

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
                guess = int(input("Please enter your 4 digit number: "))
                if len(str(guess)) != 4:
                    print("Must be 4 digits long")

            break
        except ValueError:
            print("must be an Integer")
    return guess

def make_list(data):
    this_list = []
    string = str(data)
    this_list = [char for char in string]
    return this_list

def check_answer(code, guess):
    b = 0
    c = 0
    code_list = make_list(code)
    guess_list = make_list(guess)
    remain_code_list = code_list
    remain_guess_list = guess_list
    match_list = []

    if guess == code:
        print("Well done, you broke the code!")
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



# welcome_banner()
# code = generate_code(4)
# guess = get_player_guess()

code = 1548
guess = 1434

hit, miss = check_answer(code, guess)
print(hit, miss)