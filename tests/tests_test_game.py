import pytest
from ..app import choose_word, WORDS_LIST, \
calculate_score, create_game, MAX_AMOUNT_OF_ATTEMPS, Result, next_step

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

    
    

