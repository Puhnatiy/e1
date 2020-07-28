import pytest
from enum import Enum
import time
import random
#from app import choose_word, WORDS_LIST, \
#calculate_score, create_game, MAX_AMOUNT_OF_ATTEMPS, Result, next_step
WORDS_LIST = ['skillfactory', 'testing', 'blackbox', 'pytest', 'unittest', 'coverage']
MAX_AMOUNT_OF_ATTEMPS = 4
def next_step(result):
    if result == Result.WIN:
        print("You win")
    elif result == Result.FAIL:
        print("You lost")
    else:
        time.sleep(0.1)
        return True
class Result(Enum):
    FAIL = 0
    WIN = 1
    CONTINUE = -1
class Game():
    def __init__(self):
        self.answer = choose_word(WORDS_LIST)
        self.guess_count = 0
        self.guessed_letters = []

    def guess(self, letter):
        if not letter.isalpha():
            raise ValueError
        if self.get_result() != Result.CONTINUE:
            raise ValueError
        self.guessed_letters.append(letter)
        if letter.lower() in self.answer:
            return True
        else:
            self.guess_count += 1
            return False

    def get_current_state(self):
        current_state = []
        for i in self.answer:
            if i in self.guessed_letters:
                current_state.append(i)
            else:
                current_state.append('_')
        return ''.join(current_state)

    def get_result(self):
        if self.guess_count >= MAX_AMOUNT_OF_ATTEMPS:
            return Result.FAIL
        elif self.answer == self.get_current_state():
            return Result.WIN
        else:
            return Result.CONTINUE

def create_game():
    game = Game()
    return game

def choose_word(word_list):
    return random.choice(word_list)
def calculate_score(wrong_guesses):
    return max(MAX_AMOUNT_OF_ATTEMPS - wrong_guesses, 0)
    
    

def test_choose_word():
    random_word = choose_word(WORDS_LIST)
    assert random_word in WORDS_LIST

def test_calcualte_score_positive():
    score = calculate_score(1)
    assert score == 3

def test_calcualte_score_negative():
    score = calculate_score(5)
    assert score == 0

def test_create_game():
    game = create_game()
    assert game.answer in WORDS_LIST
    assert game.guess_count == 0
    assert game.guessed_letters == []

def test_guess_not_a_letter():
    game = create_game()
    with pytest.raises(ValueError):
        game.guess("1")

def test_guess_game_over():
    game = create_game()
    game.guess_count = MAX_AMOUNT_OF_ATTEMPS + 1
    with pytest.raises(ValueError):
        game.guess("a")
    
def test_guess_success():
    game = create_game()
    answer = game.answer
    result = game.guess(answer[0])
    assert result
    assert game.guess_count == 0 
    assert answer[0] in game.guessed_letters
    assert game.get_current_state().startswith(answer[0])

def test_guess_not_success():
    game = create_game()
    result = game.guess('d')
    assert not result
    assert game.guess_count == 1
    assert 'd' in game.guessed_letters
    assert game.get_current_state() == '_'*len(game.answer)

@pytest.mark.parametrize("attempts_number", [MAX_AMOUNT_OF_ATTEMPS, MAX_AMOUNT_OF_ATTEMPS+1])
def test_get_result_fail(attempts_number):
    game = create_game()
    game.guess_count = attempts_number 
    assert game.get_result() == Result.FAIL

@pytest.mark.parametrize("attempts_number", [0, MAX_AMOUNT_OF_ATTEMPS - 1])
def test_get_result_continue(attempts_number):
    game = create_game()
    game.guess_count = attempts_number 
    assert game.get_result() == Result.CONTINUE

@pytest.mark.parametrize("attempts_number", [0, MAX_AMOUNT_OF_ATTEMPS - 1])
def test_get_result_win(attempts_number):
    game = create_game()
    game.guess_count = attempts_number 
    answer = game.answer
    game.guessed_letters = list(answer)
    assert game.get_result() == Result.WIN

@pytest.mark.parametrize("result", [Result.WIN, Result.FAIL])
def test_no_next_step(result):
    next_step_needed = next_step(result)
    assert not next_step_needed

def test_next_step():
    result = Result.CONTINUE
    next_step_needed = next_step(result)
    assert next_step_needed
