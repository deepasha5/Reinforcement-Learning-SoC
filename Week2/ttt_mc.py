import numpy as np
import random


possible_actions = 9
possible_states = 3**(9)
policy = np.random.choice(possible_actions, possible_states)
value = np.random.rand(possible_states, possible_actions)
returns = np.zeros((possible_states, possible_actions) , np.float64)
freq = np.zeros((possible_states, possible_actions) , np.float64)

#This function is used to draw the board's current state every time the user turn arrives. 
def ConstBoard(board):
    print("Current State Of Board : \n\n") 
    for i in range (0,9):
        if((i>0) and (i%3)==0):
            print("\n")
        if(board[i]==0):
            print("- ",end=" ")
        if (board[i]==1):
            print("O ",end=" ") 
        if(board[i]==-1):    
            print("X ",end=" ") 
    print("\n\n") 

#This function takes the user move as input and make the required changes on the board.
def User1Turn(board):
    pos=input("Enter X's position from [1...9]: ") 
    pos=int(pos) 
    if(board[pos-1]!=0):
        print("Wrong Move!!!") 
        exit(0)  
    board[pos-1]=-1 



#MinMax function.
def minimax(board,player):
    x=analyzeboard(board) 
    if(x!=0):
        return (x*player) 
    pos=-1 
    value=-2 
    for i in range(0,9):
        if(board[i]==0):
            board[i]=player 
            score=-minimax(board,(player*-1)) 
            if(score>value):
                value=score 
                pos=i 
            board[i]=0 

    if(pos==-1):
        return 0 
    return value 
    
#This function makes the computer's move using minmax algorithm.
def CompTurn(board):
    pos=-1 
    value=-2 
    for i in range(0,9):
        if(board[i]==0):
            board[i]=1 
            score=-minimax(board, -1) 
            board[i]=0 
            if(score>value):
                value=score 
                pos=i 
 
    board[pos]=1 

def trainTurn(board, num):
  
    curr_state = get_state(board)
    i = policy[curr_state] 
    while(board[i] !=0):
        i= np.random.choice(possible_actions)
    #print(i)
    action =i
    board[i]=num 
    next_state = get_state(board)
    reward= analyzeboard(board)
    
    freq[curr_state][action] =freq[curr_state][action]  +1
    returns[curr_state][action]= returns[curr_state][action]+ reward
    value[curr_state][action] = returns[curr_state][action]/ freq[curr_state][action]

    


#This function is used to analyze a game.
def analyzeboard(board):
    cb=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]] 

    for i in range(0,8):
        if(board[cb[i][0]] != 0 and
           board[cb[i][0]] == board[cb[i][1]] and
           board[cb[i][0]] == board[cb[i][2]]):
            return board[cb[i][2]] 
    return 0 

def get_state(board):
		# returns the current state, represented as an int
		cell = 0
		state = 0

		for i in range(3):
			for j in range(3):
				if (board[3*i+j] == 1):
					val = 1
				elif (board[3*i+j] == -1):
					val = 2
				else:
					val = 0

				state += (3^cell)*val
				cell+=1

		return state

#Main Function.
def main():
    print("training phase...")
    T = 1000
    eps =0.01
    for i in range (T):
        
        board=[0,0,0,0,0,0,0,0,0]
        player =1
        for i in range (0,9):
            if(analyzeboard(board)!=0):
                break 
            if((i+player)%2==0):
                trainTurn(board, 1) 
            else:
                trainTurn(board , -1)

        for i in range(possible_states):
            max_val =0
            opt_action =0
            for j in range(possible_actions):
                if (value[i][j]> max_val):
                    max_val =value[i][j]
                    opt_action=j  
           
            num=  random.uniform(0,1)
            if (num <= 1-eps+ (eps/possible_actions)):
                policy[i]= opt_action

            
            else:
                act= np.random.choice(possible_actions)
                while(act == opt_action):
                    act= np.random.choice(possible_actions)
                
                policy[i]= act
            
    print("training complete...")
    
    choice=1
    #The broad is considered in the form of a single dimentional array.
    #One player moves 1 and other move -1.
    board=[0,0,0,0,0,0,0,0,0] 
    if(choice==1):
        print("Computer : O Vs. You : X") 
        player= input("Enter to play 1(st) or 2(nd) :") 
        player = int(player) 
        for i in range (0,9):
            if(analyzeboard(board)!=0):
                break 
            if((i+player)%2==0):
                CompTurn(board) 
            else:
                ConstBoard(board) 
                User1Turn(board)  
         

    x=analyzeboard(board) 
    if(x==0):
         ConstBoard(board) 
         print("Draw!!!")
    if(x==-1):
         ConstBoard(board) 
         print("X Wins!!! Y Loose !!!")
    if(x==1):
         ConstBoard(board) 
         print("X Loose!!! O Wins !!!!")
       
#---------------#
main()
#---------------#

