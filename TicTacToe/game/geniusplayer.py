import math
from random import choice

class GeniusComputerPlayer():

    def __init__(self,letter,board,available_pos,game_tie):
        self.letter=letter
        self.current_winner=""
        self.board=board
        self.game_tie=game_tie
        self.available_pos=available_pos

    # Register the letter to board
    def add_letter(self,pos,letter):
        self.board[pos]=letter
        row_index=pos//3;
        col_index=pos%3;
        #Remove the position from available position container.
        self.available_pos=self.available_pos.replace(str(pos),"")

        # If current move decided the winner show it.
        # Else contiue the game.
        if self.getMoveResult(row_index,col_index,letter):
            self.current_winner=letter

    # Rwmove the letter form board.
    def remove_letter(self,pos):
        self.board[pos]=""
        self.current_winner=""
        self.game_tie=False

        #Add the position to avilable position container.
        self.available_pos+=str(pos)

    def getMoveResult(self,row_index,col_index,letter):
        letter_wins=True
        #row check
        for col in range(0,3):
            index=3*row_index+col
            if(self.board[index].strip()!=letter):
                letter_wins=False
                break

        if not letter_wins:
            #column check
            letter_wins=True
            for row in range(0,3):
                index=3*row+col_index
                if(self.board[index].strip()!=letter):
                    letter_wins=False
                    break
        #dialognal check
        #diagonal check needed when letter is in corner or in middle
        #if letter is in the middle of board then there are two diagonal check else one diagonal check 
        if not letter_wins:
            if not ((row_index==1 and col_index!=1) or (row_index!=1 and col_index==1)):
                if row_index==col_index:
                    letter_wins=True
                    for index in range(0,3):
                        index2=3*index+index
                        if(letter!=self.board[index2].strip()):
                            letter_wins=False
                            break
                if (row_index!=col_index) or row_index==1 :
                    letter_wins=True
                    for index in range(0,3):
                        index2=3*index+(3-index-1)
                        if(letter!=self.board[index2].strip()):
                            letter_wins=False
                            break
        if not letter_wins and len(self.available_pos)==0:
            self.game_tie=True
        return letter_wins
        
    #Initiate the move
    def make_move(self):
        if(len(self.available_pos)>=9):
            return int(choice(self.available_pos))
        else:
            max_player=self.letter
            min_player="X" if self.letter=="O" else "O"
            self.current_winner=""
            return self.minmax(max_player,min_player,0,True)["position"]

    def minmax(self,max_player,min_player,depth,max_player_move):

        # Base condition
        #If winner is max_player then return the score (10-depth)
        #If winner is min_player then return the score (-10+depth)
        #If game is tie  then return the score 0

        if self.current_winner==max_player:
            return {"position":None,"score":(10-depth)}
        elif self.current_winner==min_player:
            return {'position':None,"score":-10+depth}
        elif self.game_tie:
            return {'position':None,"score":0}
        

        if max_player_move:

            #Initiate the best score for max_player with -Inifinity  
            best_score={"position":None,"score":-math.inf}

            for pos in range(0,9):

                #Loop inside only if board does not contain any letter at that pos.
                if(self.board[pos]==""):

                    #Call function to register the move in board
                    self.add_letter(pos,max_player)
                    sim_score=self.minmax(max_player,min_player,depth+1,False)

                    #if current move score is greater than best score replace it and also store that position.
                    if(sim_score["score"]>best_score["score"]):
                        best_score["score"]=sim_score["score"]
                        best_score["position"]=pos

                    #Call the function to remove the letter.
                    self.remove_letter(pos)
            return best_score
                    
        else:
            #Initiate the best score for max_player with Inifinity  
            best_score={"position":None,"score":math.inf}
            for pos in range(0,9):

                 #Loop inside only if board does not contain any letter at that pos.
                if(self.board[pos]==""):

                     #Call function to register the move in board
                    self.add_letter(pos,min_player)
                    sim_score=self.minmax(max_player,min_player,depth+1,True)

                     #if current move score is less than best score replace it and also store that position.
                    if(sim_score["score"]<best_score["score"]):
                        best_score["score"]=sim_score["score"]
                        best_score["position"]=pos

                    #Call the function to remove the letter.
                    self.remove_letter(pos)
            return best_score
            


