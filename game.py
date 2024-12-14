import numpy as np
import random


class Game:
    # Creating a board upon calling
    def __init__(self):
        self.board = np.zeros((3,3))
        self.turn = -1
        self.done = []
        self.no = 0
        self.win = False
        self.ai = True


    def mode(self):
        try:
            m = int(input("Enter 1 for AI and 2 for 2 players: "))
            if(m == 2): self.ai = False
        except ValueError or TypeError:
            print("Enter either 1 or 2")


    # Declare player turn
    def declare(self):
        if(self.turn == -1):
            print("It's Player 1's turn (  O  )")
        else:
            print("It's player 2's turn (  X  )") 

    # Then a method to allow a turn
    def player_turn(self):
        print("Enter position")
        try:
            x = int(input())
            if x in self.done or x < 1 or x > 9:
                raise AssertionError
            else:
                self.done.append(x)
        
            i = (x//3) if x%3 != 0 else (x//3) - 1
            j = (x%3) - 1
            self.board[i,j] = self.turn
            self.turn *= -1
            self.no += 1

        except AssertionError:
            print("You cannot overwrite another player's move! / Don't make out of range moves")
    
        except TypeError:
            print("Enter integer position.")


    def RandomAI(self):
        return random.randint(1,9)
    
    def ai_turn(self):
        try:
            x = self.RandomAI()
            if x in self.done:
                raise AssertionError
            self.done.append(x)
            i = (x//3) if x%3 != 0 else (x//3) - 1
            j = (x%3) - 1
            self.board[i,j] = self.turn
            self.turn *= -1
            self.no += 1
        except AssertionError:
            pass


    def display(self):
        for i in range(3):
            for j in range(3):
                if(self.board[i,j] == -1):
                    print(" O ",end='')
                elif(self.board[i,j] == 1):
                    print(" X ",end="")
                else:
                    print(" _ ",end="")
            print("")

    def win_check(self):
        if(self.board[0,0] == self.board[0,1] and self.board[0,1] == self.board[0,2] and self.board[0,0] != 0):
            self.win = True
        elif(self.board[1,0] == self.board[1,1] and self.board[1,1] == self.board[1,2]  and self.board[1,0] != 0):
            self.win = True
        elif(self.board[2,0] == self.board[2,1] and self.board[2,1] == self.board[2,2]  and self.board[2,0] != 0):
            self.win = True
        elif(self.board[0,0] == self.board[1,0] and self.board[1,0] == self.board[2,0]  and self.board[0,0] != 0):
            self.win = True
        elif(self.board[0,1] == self.board[1,1] and self.board[1,1] == self.board[2,1]  and self.board[0,1] != 0):
            self.win = True
        elif(self.board[0,2] == self.board[1,2] and self.board[1,2] == self.board[2,2]  and self.board[0,2] != 0):
            self.win = True
        elif(self.board[0,0] == self.board[1,1] and self.board[1,1] == self.board[2,2]  and self.board[0,0] != 0):
            self.win = True
        elif(self.board[0,2] == self.board[1,1] and self.board[1,1] == self.board[2,0]  and self.board[0,2] != 0):
            self.win = True
        else:
            return
             
    def game_loop(self):
        self.mode()
        while(self.no < 9):
            self.display()
            self.declare()
            if(self.ai == True and self.no%2 == 1):
                self.ai_turn()
            else:
                self.player_turn()
            print(f"Turns {self.no}")
            self.win_check()
            if(self.win == True):
                self.turn *= -1
                if(self.turn == -1):
                    self.display()
                    print("Player 1 Wins!")
                    quit()
                else:
                    self.display()
                    print("Player 2 Wins!")
                    quit()
        self.display()
        print("The Match is Drawn")
    

def main():
    NewGame = Game()
    NewGame.game_loop()


if __name__ == "__main__":
    main()

