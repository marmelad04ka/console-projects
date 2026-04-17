from enum import Enum
import random
from typing import List


class Texts(Enum):
    FIRST_WELCOME = 'Welcome to the Number Guessing Game!'
    SECOND_WELCOME = 'I\'m thinking of a number between 1 and 100.'
    SELECT_DIFFICULTY = 'Please select the difficulty level:'
    CHANCES_LABEL = 'chances'
    ENTER_CHOICE = 'Enter your choice: '
    ERROR_INPUT_NOT_NUMBER = 'Please enter a valid number!'
    ERROR_INPUT_NUMBER = 'Please enter a number between {value1} and {value2}'
    GREAT_SELECTED = 'Great! You have selected the {value} difficulty level.'
    INFO_FOR_QUANTITY = 'You have {value} chances to guess the correct number.'
    LETS_START = 'Let\'s start the game!'
    ENTER_GUESS = 'Enter your guess: '
    WIN_MESSAGE = 'Congratulations! You guessed the correct number in {value} attempts.'
    NUMBER_LESS = 'Incorrect! The number is less than'
    NUMBER_GREATER = 'Incorrect! The number is greater than'
    CHECK_TRY_AGAIN = 'Please, enter "y" or "n"'
    TRY_AGAIN = 'Do you want to play it again? (y/n) '
    END_GAME = 'You\'ve wasted all your attempts and still haven\'t guessed the word!'
    GOOD_LUCK = 'Good luck!'
    YOUR_BEST_RESULTS = 'Your best results:'
    NO_DATA = 'no data'
    HIDDEN_NUMBER = 'The hidden number'
    CLUE_QUESTION = 'Want to get tips when things get tough ? (y/n) '
    CLUE_FIRST = 'The number is somewhere in {value} half'
    CLUE_SECOND = 'I think the number is somewhere in {value} quarters'
    CLUE_THIRD = 'Hmm, maybe the number in {value} ten'
    CLUE_FOUR_PREFIX = 'Something tells me this number is somewhere around here:'
    FIRST = 'first'
    SECOND = 'second'


name_difficulty_level = {'Easy': 10, 'Medium': 5, 'Hard': 3}
try_counter = {'Easy': 99, 'Medium': 99, 'Hard': 99}


def print_welcome(first_line: str, second_line: str) -> None:
    """Prints the welcome message with two lines of text"""
    print(f'{first_line}\n{second_line} \n')


def prompt_for_number(max_choice: int, text_input: str, error_number_between: str, error_input_not_number: str) -> int:
    """
        Prompts user for a number within specified range and validates input

        Args:
            max_choice: Maximum allowed value
            text_input: Prompt message to display
            error_number_between: Error message when number is out of range
            error_input_not_number: Error message when input is not a number

        Returns:
            Valid integer chosen by user within range 1..max_choice
    """
    while True:
        try:
            user_choice = int(input(text_input))
            if 1 <= user_choice <= max_choice:
                return user_choice
            else:
                print(error_number_between, '\n')
        except ValueError:
            print(f'{error_input_not_number} \n')


def prompt_yes_no(text_input: str, error_input: str) -> str:
    """
    Prompts user for yes/no answer

    Args:
        text_input: Question to display
        error_input: Error message when input is not 'y' or 'n'

    Returns:
        'y' or 'n' based on user input
    """
    while True:
        user_choice = str(input(text_input))
        if user_choice == 'y' or user_choice == 'n':
            print()
            return user_choice
        else:
            print(f'{error_input} \n')


def get_difficulty_choice() -> int:
    """Gets and validates user's difficulty level choice (1-3)"""
    max_choice = len(name_difficulty_level)

    return prompt_for_number(
        max_choice=max_choice,
        text_input=Texts.ENTER_CHOICE.value,
        error_number_between=Texts.ERROR_INPUT_NUMBER.value.format(value1='1', value2=max_choice),
        error_input_not_number=Texts.ERROR_INPUT_NOT_NUMBER.value
    )


def print_difficulty_menu(select_difficulty_line: str, chances_label: str) -> None:
    """Displays the difficulty selection menu with available options"""
    print(f'{select_difficulty_line}')

    for index, (level_name, chances) in enumerate(name_difficulty_level.items(), start=1):
        print(f'{index}. {level_name} ({chances} {chances_label})')

    print()


def get_difficulty(choice: int) -> str:
    """Returns the difficulty level name based on user's choice (1-based index)"""
    return list(name_difficulty_level.keys())[choice - 1]


def setup_game_session(choice: int) -> str:
    """
    Sets up game session with chosen difficulty and clue preference

    Args:
        choice: User's difficulty choice (1-3)

    Returns:
        'y' or 'n' indicating if user wants clues
    """
    diff = get_difficulty(choice)

    print(Texts.GREAT_SELECTED.value.format(value=diff))
    print(Texts.INFO_FOR_QUANTITY.value.format(value=name_difficulty_level[diff]))

    print()
    clue = prompt_yes_no(Texts.CLUE_QUESTION.value, Texts.CHECK_TRY_AGAIN.value)

    return clue


def get_guess() -> int:
    """Gets and validates user's number guess (1-100)"""
    return prompt_for_number(
        max_choice=100,
        text_input=Texts.ENTER_CHOICE.value,
        error_number_between=Texts.ERROR_INPUT_NUMBER.value.format(value1='1', value2=100),
        error_input_not_number=Texts.ERROR_INPUT_NOT_NUMBER.value
    )


def print_goodbye(text: str) -> None:
    """Prints farewell message"""
    print(text)


def display_leaderboard() -> None:
    """Displays the best scores for each difficulty level"""
    print(f'{Texts.YOUR_BEST_RESULTS.value} \n')

    for index, (level_name, score) in enumerate(try_counter.items(), start=1):
        if score == 99:
            print(f'{index}. {level_name} - {Texts.NO_DATA.value}')
            continue
        print(f'{index}. {level_name} - {score}')

    print()


def get_decade(secret_number: int) -> int:
    """Returns the index of the top ten (0-9) for the number 1-100"""
    return (secret_number - 1) // 10


def get_shuffled_triplet(secret_number: int, index_for_lot: int) -> List[int]:
    """
    Generates a shuffled triplet containing the secret number and two random numbers

    Args:
        secret_number: The hidden number to guess
        index_for_lot: Index of the ten range (0-9) where secret number is located

    Returns:
        List of 3 numbers in random order, containing secret_number and 2 random numbers
    """
    left = index_for_lot * 10 + 1
    right = index_for_lot * 10 + 10

    while True:
        random_number_one = random.randint(left, right)
        if random_number_one != secret_number:
            break

    while True:
        random_number_two = random.randint(left, right)
        if random_number_two != secret_number and random_number_two != random_number_one:
            break

    arr = [
        [random_number_one, secret_number, random_number_two],
        [random_number_two, random_number_one, secret_number],
        [secret_number, random_number_two, random_number_one]
    ]

    return random.choice(arr)


def get_quarter(secret_number: int) -> int:
    """Returns the quarter number (1-4) for the number 1-100"""
    return (secret_number - 1) // 25 + 1


def show_hint(counter: int, max_try: int, secret_number: int, clue: str) -> None:
    """
        Provides progressive hints as player runs out of attempts

        Args:
            counter: Current attempt number
            max_try: Maximum allowed attempts
            secret_number: The hidden number to guess
            clue: 'y' if hints are enabled, 'n' otherwise
        """
    if clue != 'y':
        return
    number = max_try - counter
    list_of_tens = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth']
    index_for_lot = get_decade(secret_number)

    if counter >= max_try/2:
        if number == 4:
            print(Texts.CLUE_FIRST.value.format(value=Texts.FIRST.value if secret_number <= 50 else Texts.SECOND.value))
        if number == 3:
            quarter = get_quarter(secret_number)
            print(Texts.CLUE_SECOND.value.format(value=quarter))
        if number == 2:
            print(Texts.CLUE_THIRD.value.format(value=list_of_tens[index_for_lot]))
        if number == 1:
            three_random_number = get_shuffled_triplet(secret_number, index_for_lot)
            print(f'{Texts.CLUE_FOUR_PREFIX.value} {three_random_number[0]}, {three_random_number[1]}, {three_random_number[2]}')


def number_of_guessing_game() -> None:
    """Main game loop - orchestrates the entire Number Guessing Game"""
    print_welcome(Texts.FIRST_WELCOME.value, Texts.SECOND_WELCOME.value)

    while True:
        secret_number = random.randint(1, 100)
        counter = 0
        check_end = 0

        print_difficulty_menu(Texts.SELECT_DIFFICULTY.value, Texts.CHANCES_LABEL.value)

        choice = get_difficulty_choice()

        clue = setup_game_session(choice)

        print(Texts.LETS_START.value)
        print()

        diff = get_difficulty(choice)
        max_try = name_difficulty_level[diff]

        for _ in range(max_try):
            counter += 1
            user_number = get_guess()

            if user_number == secret_number:
                print(Texts.WIN_MESSAGE.value.format(value=counter))
                print()

                if counter < try_counter[diff]:
                    try_counter[diff] = counter

                display_leaderboard()

                try_again = prompt_yes_no(Texts.TRY_AGAIN.value, Texts.CHECK_TRY_AGAIN.value)
                if try_again == 'y':
                    check_end += 1
                    break
                else:
                    print_goodbye(Texts.GOOD_LUCK.value)
                    return
            elif user_number > secret_number:
                print(f'{Texts.NUMBER_LESS.value} {user_number}.\n')
                show_hint(counter, max_try, secret_number, clue)
            else:
                print(f'{Texts.NUMBER_GREATER.value} {user_number}.\n')
                show_hint(counter, max_try, secret_number, clue)

        if check_end == 0:
            print(f'{Texts.END_GAME.value} \n')
            print(f'{Texts.HIDDEN_NUMBER.value}: {secret_number} \n')

            try_again = prompt_yes_no(Texts.TRY_AGAIN.value, Texts.CHECK_TRY_AGAIN.value)

            if try_again == 'n':
                display_leaderboard()
                print_goodbye(Texts.GOOD_LUCK.value)
                break


if __name__ == "__main__":
    number_of_guessing_game()
