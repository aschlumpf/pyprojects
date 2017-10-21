'''
Created on Dec 7, 2016

@author: AlexS
'''
'''
Alex Schlumpf
I pledge my honor that I have abided by the Stevens Honor System
'''
class Board(object):
    def __init__(self, width=7, height=6, board=[]):
        ''' Initialize the constructor. Width and height are 7 and 6 by default, respectively. BoardTest2 is [] by default, and shouldn't be directly passed in by the user. '''
        self.width = width
        self.height = height
        self.board = self.createBoard()
    
    def createOneRow(self):
        """Returns one row of zeros of width "width"...  
           You should use this in your
           createBoard(width, height) function."""
        row = []
        for _ in range(self.width):
            row += ['']
        return row
    
    def createBoard(self):
        out = []
        for _ in range(self.height):
            out += [self.createOneRow()]
        return out

    
    def allowsMove(self, col):
        ''' Checks to see if a move is allowed given the state of the board. '''
        if col in range(self.width):
            for row in range(self.height):
                if self.board[row][col] == '':
                    return True
        return False
    
     
    def addMove(self, col, ox):
        ''' Adds a move the board, assuming the move can be made. '''
        if self.allowsMove(col):
            for row in range(self.height-1, -1, -1):
                if self.board[row][col] == '':
                    self.board[row][col] = ox
                    break
    
    def delMove(self, col):
        ''' Deletes a move from the board. '''
        if col in range(self.width):
            for row in range(self.height-1):
                if self.board[row][col] != '':
                    self.board[row][col] = ''
                    break
                
    def padBoard(self):
        ''' Pads empty strings to the head and tail of the board to prevent index errors when checking for a win. '''
        out = []
        for item in self.board:
            out.append(['']*4 + item + ['']*4)
        return [['']*(self.width+8)]*4 + out + [['']*(self.width+8)]*4
    
    def winsFor(self, ox):
        ''' Checks to see if X or O won the game. '''
        board = self.padBoard()
        for i in range(4, len(board)-4):
            for j in range(4, len(board[i])-4):
                if board[i][j] == ox:
                    if board[i+1][j] == ox and board[i+2][j] == ox and board[i+3][j] == ox:
                        return True
                    if board[i][j+1] == ox and board[i][j+2] == ox and board[i][j+3] == ox:
                        return True
                    if board[i+1][j+1] == ox and board[i+2][j+2] == ox and board[i+3][j+3] == ox:
                        return True
                    if board[i+1][j-1] == ox and board[i+2][j-2] == ox and board[i+3][j-3] == ox:
                        return True
        return False
    
    def setBoard( self, moveString ):
        """ takes in a string of columns and places
         alternating checkers in those columns,
         starting with 'X'
        
         For example, call b.setBoard('012345')
         to see 'X's and 'O's alternate on the
         bottom row, or b.setBoard('000000') to
         see them alternate in the left column.
         moveString must be a string of integers
         """
        nextCh = 'X' # start by playing 'X'
        for colString in moveString:
            col = int(colString)
            if 0 <= col <= self.width:
                self.addMove(col, nextCh)
            if nextCh == 'X': nextCh = 'O'
            else: nextCh = 'X'
    
    
    def __str__(self):
        ''' Returns the string format of the game board. '''
        board = self.board
        output = ''
        for i in range(len(board)):
            if i > 0:
                output += '\n'
            for j in range(len(board[i])):
                if board[i][j] == '':
                    output += '| '
                else:
                    output += '|' + board[i][j]
            output += '|'
            
            if i == len(board) - 1:
                output += '\n'
                for _ in range(len(board[i])):
                    output += '-'*2
                output += '-\n'
                inc = 0
                for _ in range(len(board[i])):
                    output += ' ' + str(inc)
                    inc += 1
        return output
    
    def hostGame(self):
        ''' The interface with which the user plays the game. '''
        print("Welcome to Connect Four!\n")
        while(1):
            print(self.__str__())
            print('\n')
            x = int(input("X's choice: "))
            while(x > self.width-1):
                x = int(input("\nX's choice is not possible! Try again: "))
            print('\n')
            self.addMove(x, 'X')
            if self.winsFor('X'):
                print(self.__str__())
                print("\nX Wins! -- Congratulations!")
                break
            print(self.__str__()+'\n')
            o = int(input("O's choice: "))
            while(o > self.width-1):
                o = int(input("\nO's choice is not possible! Try again: "))
            print('\n')
            self.addMove(o, 'O')
            if self.winsFor('O'):
                print(self.__str__())
                print("\nO Wins! -- Congratulations!")
                break
             
if __name__ == '__main__':
    d = Board()
    d.hostGame()
