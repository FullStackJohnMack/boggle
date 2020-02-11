from flask import Flask, render_template
from boggle import Boggle

app = Flask(__name__)


boggle_game = Boggle()


@app.route('/')
def main():
    board = boggle_game.make_board()
    return render_template("game.html", board=board)
