import random
from colorama import Fore,Style

MAX_TURN = 9

class Board:
    def __init__(self):
       self.board = [[None for _ in range(3)] for _ in range(3)]
    
    def render(self):
        print("")
        for i in range(3):
            for j in range(3):
                x = self.board[i][j] if self.board[i][j] != None else " "
                color_name = "RED" if (x == "O") else "BLUE"
                color = getattr(Fore,color_name) 

                if j != 2:
                    print(color+f" {x}",end='')
                    style_reset()
                    print(f" |",end='')
                else:
                    print(color+f" {x} ",end='')
                    style_reset()
            print('')
            if i != 2:
                print("---|"*2,end='')
                print('---')
        print('')
    
    def make_move(self,move,token):
        temp_board = self.board
        temp_board[move[0]][move[1]] = token
        self.board = temp_board
    
    def check_win(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != None:  
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != None:  
                return True

        if self.board[0][0] == self.board[1][1] == self.board[2][2] != None: 
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != None: 
            return True
                
        return False

class Player():
    
    def validate_move(self,move,board):
        if board.board[move[0]][move[1]] != None:
            return False
        return True
    
    def convert_move(self,x):
        i = (x//3) if x%3 != 0 else (x//3) - 1
        j = (x%3) - 1
        return [i,j]

    def get_move(self,board):
        while True:
            try:
                x = int(input("Make your move: "))
                if x < 1 or x > 9:
                    raise ValueError
                move = self.convert_move(x)
                if self.validate_move(move,board) == False:
                    raise AssertionError
                return move
            except ValueError:
                print("Enter a valid integer from 1 to 9.")
            except AssertionError:
                print("Please enter a square which isn't occupied.")

class AI(Player):
    def get_move(self,board):
        move = self.random_ai(board)
        return move
    
    def random_ai(self,board):
        move = [-1,-1]
        while(self.validate_move(move,board) != True):
            move = self.convert_move(random.randint(1,9))
        return move

class Interface():
    def __init__ (self,p1,p2):
        if p1 == 0:
            self.P1 = Player()
        else:
            self.P1 = AI()
        if p2 == 0:
            self.P2 = Player()
        else:
            self.P2 = AI()
        self.win = False

    def game_loop(self,board=Board()):
        board.render()
        turn = 1

        while(self.win != True and turn <= MAX_TURN):
            token = "X" if (turn%2 == 0) else "O"
            if (token == "O"):
                print("Player 1's Turn")
                move = self.P1.get_move(board)
            else:
                print("Player 2's Turn")
                move = self.P2.get_move(board)
            board.make_move(move,token)
            board.render()
            self.win = board.check_win()
            if self.win == True:
                if token == "O":
                    print(Fore.GREEN + "Player 1 wins!")
                    style_reset()
                else:
                    print(Fore.GREEN + "Player 2 wins!")
                    style_reset()
            turn += 1        

        if self.win == False:
            print("The game has been drawn.")

def style_reset():
    print(Style.RESET_ALL,end='')

def main():
    try:
        print("Enter 0 for human and 1 for computer.")
        x = int(input("Human or computer for Player 1: "))
        y = int(input("Human or computer for Player 2: "))
        game = Interface(x,y)
        game.game_loop()
    except ValueError:
        print("0 for Human and 1 for Computer.\n")
        main()

if __name__ == "__main__":
    main()
