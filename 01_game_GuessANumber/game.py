from random import randint
from easyAI import TwoPlayerGame, Human_Player, AI_Player, Negamax
"""
Instrukcja:
- instalacja pakietu easyAI (pip install easyAI)
- Lub zainstalować z pliku requirements.txt (pip install -r requirements.txt)
Autorzy: 
- Damian Brzoskowski (s18499), Rafał Sochacki (s20047)
Opis:
Gra jest wykorzystaniem popularnej gry "Zgadnij liczbę"
W tym przypadku jest to gra oparata o easyAI, która ma za zadanie wykorzystać AI do tego, aby odgadło liczbę szybciej
niż człowiek. Kto pierwszy zgadnie jaka liczba została wylosowana z przedziału od 1 do 20 ten wygrywa
"""


class GuessNumber(TwoPlayerGame):
    """ In turn, the players remove one, two or three bones from a
        pile of bones. The player who removes the last bone loses. """

    def __init__(self, players):
        """ Initialize Game objects and take players as an arg
        :param players:
        """
        self.winner = False
        self.players = players
        self.human_numbers = [i for i in range(1, 21)]  # Human numbers range
        self.ai_numbers = [i for i in range(1, 21)]  # AI numbers range
        self.current_player = 1
        self.guess_number = randint(1, 21)  # random number to guess
        self.move = None  # we must know about move

    def possible_moves(self):
        """ Possible moves to make in the game  """
        if self.player.name == 'Human':
            return self.ai_numbers
        elif self.player.name == 'AI':
            return self.human_numbers

    def make_move(self, move):
        """
        The logic of how the game moves
        :param move: Take move chosen by player and remove from possible moves
        :return: Return the list in which the number was removed
        """
        if self.player.name == 'Human':
            self.ai_numbers.remove(move)
        else:
            self.human_numbers.remove(move)
        self.move = move

    def win(self):
        """ Checks if someone is winning the match """
        return self.guess_number == self.move

    def is_over(self):
        """ Game stops when someone guess number """
        return self.win()

    def show(self):
        """ Show information about possibles moves in current round """
        if self.player.name == 'Human':
            print(f"{self.ai_numbers} {self.opponent.name} numbers left")
        if self.player.name == 'AI':
            print(f"{self.human_numbers} {self.opponent.name} numbers left")

    def scoring(self):
        """ Final points and ends the game"""
        return 100 if game.win() else 0  # For the AI


ai = Negamax(2)  # The AI will think 2 moves in advance
game = GuessNumber([Human_Player(), AI_Player(ai)])
history = game.play()