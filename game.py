import numpy as np
import itertools

def isTerminalState(game_state):
    n = len(GetPossibleMoves(game_state))
    if n==0:
        return 1
    else:
        return 0
                        
def evaluateState(game_state):
    return len(GetPossibleMoves(game_state))

def GetPossibleMoves(game_state):
	p=[]
	live_nodes=GetLiveNodes(game_state)
	for subset in itertools.combinations(live_nodes, 2):
		p.append(subset)
	return p

def GetNewGameState(game_state,move):
        l=len(game_state);
	h=np.zeros((l+1,l+1))
	h=h.astype(int)	
	k=h.tolist()
#	print k
#	indices
	for i in range(len(game_state)):
		for j in range(len(game_state)):
			k[i][j]=game_state[i][j]
	
	k[move[0]-1][l] = 1
	k[l][move[0]-1] = 1
	k[move[1]-1][l] = 1
	k[l][move[1]-1] = 1	
	print k	

	return k
	
def GetBestMove(game_state, player,depth, cur_depth):
#	Ndegrees =degrees[:]
#	Nindices =indices[:]
#	Nlive_nodes=live_nodes[:]
    possible_moves= GetPossibleMoves(game_state)
    best_move = possible_moves[0]	    
    l=len(game_state)
    if player==1:
        best=-1*3*l
    else:
        best= 3*l

    for move in possible_moves:
        new_game_state = GetNewGameState(game_state,move)
        if isTerminalState(game_state)==1:
            utility = 0
        elif cur_depth==depth:
            utility = evaluateState(game_state)
        else:
            x = GetBestMove(new_game_state, -1*player,depth, cur_depth+1)
            utility = x[1]
        if player== 1:
            if utility > best:
                best = utility
                best_move = move
        elif player == -1:
            if utility < best:
                best = utility  
                best_move = move      
    return (best_move, best)        
            	    
#		Nindices.append(Nindices[-1]+1)
#		Ndegrees.append(0)
#		Ndegrees[move[1]-1]=Ndegrees[move[1]-1]+1
#		Ndegrees[move[0]-1]=Ndegrees[move[0]-1]+1
#		Ndegrees[Nindices[-1]-1]=Ndegrees[Nindices[-1]-1]+2;
#		print(Ndegrees)
#       print move


def GetLiveNodes(game_state):
    l=[]
    for x in range(len(game_state)):
    	if sum(game_state[x]) < 3:
    		l.append(x+1)
    return l 

def main():
    n=input("Number of Sprouts: ")
    depth = input("Depth: ")
#	indices= range(1,n+1)
#	degrees= [0] * n
    g=np.zeros((n,n))
    g=g.astype(int)
    game_state=g.tolist()
    live_nodes= GetLiveNodes(game_state)
    result = GetBestMove(game_state,-1, depth,0)
    print result[0]
if __name__ == "__main__":
    main()




                
