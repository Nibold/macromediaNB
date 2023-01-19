import json
from packages.main import main


class Game:
    def __init__(self, rows, cols, p1, p2):
        self.board = [['-' for _ in range(cols)] for _ in range(rows)]
        self.rows = rows
        self.cols = cols
        self.p1 = p1
        self.p2 = p2
        self.current_player = p1
    
    def play_chip(self, col):
        for row in range(self.rows-1, -1, -1):
            if self.board[row][col] == '-':
                self.board[row][col] = self.current_player.chip
                break
        else:
            raise ValueError("Die Spalte ist voll. Fang nochmal von vorne an")
    
    def switch_players(self):
        if self.current_player == self.p1:
            self.current_player = self.p2
        else:
            self.current_player = self.p1
    
    def check_win(self):
        # Ein horizontaler Gewinn wird überprüft
        for row in range(self.rows):
            for col in range(self.cols-3):
                if self.board[row][col] == self.board[row][col+1] == self.board[row][col+2] == self.board[row][col+3] != '-':
                    return True
        
        # Ein vertikaler Gewinn wird überprüft
        for row in range(self.rows-3):
            for col in range(self.cols):
                if self.board[row][col] == self.board[row+1][col] == self.board[row+2][col] == self.board[row+3][col] != '-':
                    return True
        
        # Ein diagonaler Gewinn wird überprüft (oben links nach unten rechts)
        for row in range(self.rows-3):
            for col in range(self.cols-3):
                if self.board[row][col] == self.board[row+1][col+1] == self.board[row+2][col+2] == self.board[row+3][col+3] != '-':
                    return True
        
        # Ein diagonaler Gewinn wird überprüft (oben rechts nach unten links)
        for row in range(self.rows-3):
            for col in range(3, self.cols):
                if self.board[row][col] == self.board[row+1][col-1] == self.board[row+2][col-2] == self.board[row+3][col-3] != '-':
                    return True
        
        return False
    
    def draw(self):
        for row in self.board:
            print(' '.join(row))

    def save_state(self, filename):
        with open(filename, 'w+') as f:
            data = {
            'rows': self.rows,
            'cols': self.cols,
            'board': self.board,
            'p1': self.p1.__dict__,
            'p2': self.p2.__dict__,
            'current_player': self.current_player.__dict__
        }
            json.dump(data, f)

@classmethod
def load_state(cls, filename):
    with open(filename, 'r') as f:
        data = json.load(f)
        rows = data['rows']
        cols = data['cols']
        p1_dict = data['p1']
        p1 = Player(p1_dict['name'], p1_dict['chip'])
        p2_dict = data['p2']
        if p2_dict['name'] == 'Player 2':
            p2 = Player(p2_dict['name'], p2_dict['chip'])
        else:
            p2 = HumanPlayer(p2_dict['name'], p2_dict['chip'])
        game = cls(rows, cols, p1, p2)
        game.board = data['board']
        current_player_dict = data['current_player']
        if current_player_dict['name'] == p1.name:
            game.current_player = p1
        else:
            game.current_player = p2
        return game


class Player:
    def __init__(self, name, chip):
        self.name = name
        self.chip = chip

class HumanPlayer(Player):
    def __init__(self, name, chip):
        super().__init__(name, chip)
        
    def get_move(self):
        col = int(input(f"{self.name}, choose a column (1-7): ")) - 1
        return col

def main():
    # kreiere Spieler
    p1 = Player("Player 1", "X")
    p2 = HumanPlayer("Player 2", "O")
    
    # kreiere Spiel
    game = Game(6, 7, p1, p2)
    
    # Hauptspiel loop
    while True:
        # print Zug des aktuellen Spielers
        print(f"{game.current_player.name} ist dran. Wer wird 4 gewinnt gewinnen?")
        
        # print Brett
        game.draw()
        
        # den Zug des Spielers erhalten
        if game.current_player == p1:
            while True:
                try:
                    col = int(input("P1 hat das 'X' and P2 das 'O' - Welche Spalte (1-7) möchtest du wählen? ")) - 1
                    game.play_chip(col)
                except ValueError as e:
                    print(e)
                else:
                    break
        else:
            col = game.current_player.get_move()
            game.play_chip(col)
        
        # speichern des Spielstandes
        game.save_state('game.json')

        # Überprüfung auf Gewinn
        if game.check_win():
            game.draw()
            print(f"{game.current_player.name} hat gewonnen!")
            break
        
        # Spieler wechseln
        game.switch_players()

if __name__ == '__main__':
    main()