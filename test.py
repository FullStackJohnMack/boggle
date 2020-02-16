from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

# Arrange, act, assert


class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_main(self):
        """Test if home route is loading intro HTML score element"""
        with self.client:
            response = self.client.get('/')
            self.assertIn(b'<h3 id="high_score">', response.data)

    def test_valid_word(self):
        """Test if word is valid by modifying the board in the session"""
        with self.client:
            with self.client.session_transaction() as session:
                session['board'] = [["C", "A", "T", "T", "T"],
                                    ["C", "A", "T", "T", "T"],
                                    ["C", "A", "T", "T", "T"],
                                    ["C", "A", "T", "T", "T"],
                                    ["C", "A", "T", "T", "T"]]
            response = self.client.get('/check-word?word=cat')
        self.assertEqual(response.json['result'], 'ok')

    def test_end_game(self):
        """Test if game count is incrementing after each game"""
        with self.client:
            response = self.client.get('/end-game?is_this_high_score=0')
        self.assertEqual(response.json['game_count'], 1)

    def test_check_high_score(self):
        """Test if high score is being recorded in session"""
        with self.client:
            with self.client.session_transaction() as change_session:
                change_session['high_score'] = "999"
                change_session['is_this_high_score'] = "1"
            response = self.client.get("/check-high-score")
            self.assertEqual(response.data, b'999')

    def test_invalid_word(self):
        """Test if word is in the dictionary but not on the board"""
        self.client.get('/')
        response = self.client.get('/check-word?word=impossible')
        self.assertEqual(response.json['result'], 'not-on-board')

    def test_nonsense_word(self):
        """Test if nonsense word is not in the dictionary"""
        self.client.get('/')
        response = self.client.get('/check-word?word=fsdfgsfgsfdgfg543')
        self.assertEqual(response.json['result'], 'not-word')
