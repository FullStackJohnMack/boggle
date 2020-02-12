from flask import Flask, render_template, session, request, redirect
from boggle import Boggle


app = Flask(__name__)
app.config["SECRET_KEY"] = "password"

boggle_game = Boggle()


@app.route('/')
def main():
    board = boggle_game.make_board()
    session['board'] = board
    return render_template("game.html", board=board)


@app.route('/check-word')
def check_word():
    word = request.args["word"]
    board = session['board']
    result = {"result": f"{boggle_game.check_valid_word(board, word)}"}
    return result
