import random
from colorama import Fore,Style
from copy import deepcopy
import json  


# Add AI player repeated battles and average calculator.


# Constants
MAX_TURN = 9
FIRST_TOKEN = "O"
SECOND_TOKEN = "X"
AI_NO = 4

# Main Board class
class Board:
    def __init__(self):
       self.board = [[None for _ in range(3)] for _ in range(3)]
       self.current_player = FIRST_TOKEN

    # renders or prints the board    
    def render(self):
        print("")
        for i in range(3):
            for j in range(3):
                x = self.board[i][j] if self.board[i][j] != None else " "
                color_name = "RED" if (x == FIRST_TOKEN) else "BLUE"
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
    
    # makes the move on board
    def make_move(self,move,token):
        temp_board = self.board
        temp_board[move[0]][move[1]] = token
        self.board = temp_board
    
    # checks for win
    def check_win(self,token):
        for i in range(3):
            if token == self.board[i][0] == self.board[i][1] == self.board[i][2] != None:  
                return True
            if token == self.board[0][i] == self.board[1][i] == self.board[2][i] != None:  
                return True

        if token == self.board[0][0] == self.board[1][1] == self.board[2][2] != None: 
            return True
        if token == self.board[0][2] == self.board[1][1] == self.board[2][0] != None: 
            return True
                
        return False
    

    # returns winner for minimax AI
    def return_winner(self,player_to_optimize):
        opponent = FIRST_TOKEN if player_to_optimize == SECOND_TOKEN else SECOND_TOKEN
        if self.check_win(player_to_optimize):
            return 10
        elif self.check_win(opponent):
            return -10
        else: 
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == None:
                        return None
            return 0
    
    # Gives all legal moves in a list
    def get_legal_moves(self):
        legal_moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == None:
                    legal_moves.append([i,j])
        return legal_moves

    # copys the whole board class and makes a move
    def copy_and_make_move(self,move,current_player):
        temp_board = deepcopy(self)
        temp_board.board[move[0]][move[1]] = current_player
        return temp_board


# Player class
class Player():
    # checks if move is valid
    def validate_move(self,move,board):
        if board.board[move[0]][move[1]] != None:
            return False
        return True
    # converts move from number to coord
    def convert_move(self,x):
        i = (x//3) if x%3 != 0 else (x//3) - 1
        j = (x%3) - 1
        return [i,j]

    # takes input
    def get_move(self,board,current_player):
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

# AI Class inherited from player
class AI(Player):

    def __init__(self,z):
        super().__init__()
        self.ai_choice = z
        self.cache = {} # cache for minimax AI
        self.ai_win = False # Win condition
        self.AIs = [self.random_ai,self.find_winning_move_ai,self.find_winning_and_losing_move_ai,self.minimax_ai] # List of all AIs


    def get_move(self,board: Board,current_player):
        move = self.AIs[self.ai_choice-1](board,current_player)
        return move

    # Randomly gives a legal move.    
    def random_ai(self,board: Board,current_player):
        possible_moves = [[i, j] for i in range(3) for j in range(3) if board.board[i][j] is None]
        random.shuffle(possible_moves)
        return possible_moves[0]
    
    # Finds a winning move and then makes it
    def find_winning_move_ai(self,board: Board,current_player):
        for i in range(3):
            for j in range(3):
                if board.board[i][j] is None:
                    board.board[i][j] = current_player
                
                    if board.check_win(current_player):
                        board.board[i][j] = None
                        self.ai_win = True
                        return [i,j]
                    
                    board.board[i][j] = None
        
        return self.random_ai(board,current_player)

    # Finds a winning move and blocks your winning move.
    def find_winning_and_losing_move_ai(self,board: Board,current_player):
        move = self.find_winning_move_ai(board,current_player)
        if(self.ai_win == True):
            return move
        else:
            opponent = FIRST_TOKEN if current_player == SECOND_TOKEN else SECOND_TOKEN
            for i in range(3):
                for j in range(3):
                    if board.board[i][j] is None:
                        board.board[i][j] = opponent
                        if board.check_win(opponent):
                            board.board[i][j] = None
                            return [i,j]
                        board.board[i][j] = None
            
            return self.random_ai(board,current_player)

    # Calculates the score of all states.
    def minimax_score(self,board: Board,current_player,player_to_optimize):
        if board.return_winner(player_to_optimize) != None:
            return board.return_winner(player_to_optimize)
        scores = []
        for move in board.get_legal_moves():
            new_board = board.copy_and_make_move(move,current_player)
            opponent = FIRST_TOKEN if current_player == SECOND_TOKEN else SECOND_TOKEN
            score = self.minimax_score(new_board,opponent,player_to_optimize)
            scores.append(score)
            
        if current_player == player_to_optimize:
            return max(scores)
        else:
            return min(scores)
        
    # Makes a move according to minimax_score
    def minimax_ai(self,board: Board, current_player):
        best_move = None
        best_score = None
        for move in board.get_legal_moves():
            new_board = board.copy_and_make_move(move,current_player)
            opponent = FIRST_TOKEN if current_player == SECOND_TOKEN else SECOND_TOKEN
            score = self.minimax_score_with_cache(new_board,opponent,current_player)
            if best_score is None or score > best_score:
                best_move = move
                best_score = score
            
        return best_move
    
    # More efficient compared to bruteforce minimax.
    def minimax_score_with_cache(self,board:Board,current_player,player_to_optimize):
        board_cache_key = str(board.board)
        if board_cache_key not in self.cache:
            score = self.minimax_score(board,current_player,player_to_optimize)
            self.cache[board_cache_key] = score
            
        return self.cache[board_cache_key]


# Game Interface which takes two players, can be AI or player.
class Game():
    def __init__ (self,p1,p2,z1,z2):
        if p1 == 0:
            self.P1 = Player()
        else:
            self.P1 = AI(z1)
        if p2 == 0:
            self.P2 = Player()
        else:
            self.P2 = AI(z2)
        self.win = False
    # Core Game Loop
    def game_loop(self,board=Board()):
        board.render()
        turn = 1

        while(self.win != True and turn <= MAX_TURN):
            self.current_player = SECOND_TOKEN if (turn%2 == 0) else FIRST_TOKEN
            if (self.current_player == FIRST_TOKEN):
                print("Player 1's Turn")
                move = self.P1.get_move(board,self.current_player)
            else:
                print("Player 2's Turn")
                move = self.P2.get_move(board,self.current_player)
            board.make_move(move,self.current_player)
            board.render()
            self.win = board.check_win(self.current_player)
            if self.win == True:
                if self.current_player == FIRST_TOKEN:
                    print(Fore.GREEN + "Player 1 wins!")
                    style_reset()
                else:
                    print(Fore.GREEN + "Player 2 wins!")
                    style_reset()
            turn += 1        

        if self.win == False:
            print("The game has been drawn.")

# Resets colors
def style_reset():
    print(Style.RESET_ALL,end='')

def main():
    # Menu for Player selection
    try:
        print("Enter 0 for human and 1 for computer.")
        x = int(input("Human or computer for Player 1: "))
        if(x == 1):
            print("Enter your choice for AI")
            print("1 for Random AI")
            print("2 for Find Winning Moves AI")
            print("3 for Find Winnning and Losing Moves AI")
            print("4 for Minimax AI")
            z1 = int(input("Choice: "))
            if z1 not in range(1,AI_NO+1):
                raise AssertionError
        else:
            z1 = 0
        y = int(input("Human or computer for Player 2: "))
        if(y == 1):
            print("Enter your choice for AI")
            print("1 for Random AI")
            print("2 for Find Winning Moves AI")
            print("3 for Find Winnning and Losing Moves AI")
            print("4 for Minimax AI")
            z2 = int(input("Choice: "))
            if z2 not in range(1,AI_NO+1):
                raise AssertionError
        else:
            z2 = 0
        game = Game(x,y,z1,z2)
        game.game_loop()
    except ValueError:
        print("0 for Human and 1 for Computer.\n")
        main()
    except AssertionError:
        print("Enter valid choice for AI")
        main()

if __name__ == "__main__":
    main()


