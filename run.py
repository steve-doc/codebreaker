from random import randrange

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
    while True:
        try:
            guess = 0
            while len(guess) != 4:
                guess = int(input("Please enter your 4 digit number: "))
                if len(guess) != 4:
                    print("Must be 4 digits long")

            break
        except ValueError:
            print("must be an Integer")
    print(guess)
# code = generate_code(4)
get_player_guess()