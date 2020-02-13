from flask import Flask, render_template, session, request, redirect, flash
from boggle import Boggle


app = Flask(__name__)
app.config["SECRET_KEY"] = "password"

boggle_game = Boggle()
entered_words = []


@app.route('/')
def main():
    """Initializes the game and renders the game board HTML"""
    board = boggle_game.make_board()
    session['board'] = board
    session['completed_games'] = 0
    return render_template("game.html", board=board)


@app.route('/check-word')
def check_word():
    """Checks if a word is in the dictionary and on the board or if that word has already been used"""
    word = request.args["word"]
    board = session['board']
    result = {"result": f"{boggle_game.check_valid_word(board, word)}"}
    if word in entered_words:
        result = {"result": "already-in-list"}
    else:
        entered_words.append(word)
    return result


@app.route('/end-game')
def end_game():
    """Handles end of game actions and returns an object with the current number of completed games"""
    is_this_high_score = request.args["is_this_high_score"]
    session["is_this_high_score"] = is_this_high_score
    game_count = incrementGameCount()
    result = {
        "game_count": game_count
    }
    return result


@app.route('/check-high-score')
def check_high_score():
    """Updates high score in session between session high and this game's high and returns the current session high score"""
    if session.get("high_score") == None:
        session["high_score"] = session.get("is_this_high_score")
        high_score = session.get("is_this_high_score")
    else:
        if session.get("is_this_high_score") > session.get("high_score"):
            session["high_score"] = session.get("is_this_high_score")
    return session.get("high_score")


def incrementGameCount():
    """Updates game count in session after each game and returns the game count"""
    if session.get("game_count"):
        session["game_count"] = session["game_count"] + 1
    else:
        session["game_count"] = 1
    return session.get("game_count")


# check all docstrings, write tests for all Python views, enhance timer, refactor
