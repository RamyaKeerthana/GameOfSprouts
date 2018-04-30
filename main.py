import pygame
import math
import numpy as np
import random
import itertools


WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

class node():

    def __init__(self, no, color, center, radius, link):
        self.no = no
        self.color = color
        self.center = center
        self.radius = radius
        self.link = link


class player():

    def __init__(self, color, turn):
        self.color = color
        self.turn = turn
        self.moves = []







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
#	print k	

	return k
	
def GetBestMove(game_state, player,depth, cur_depth):
#	Ndegrees =degrees[:]
#	Nindices =indices[:]
#	Nlive_nodes=live_nodes[:]
    possible_moves= GetPossibleMoves(game_state)
    if isTerminalState(game_state)==0:
        best_move = possible_moves[0]	    
    else:
        return (-1,-1)
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

def test():
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
    game_state = GetNewGameState(game_state,result[0])

def GetMove(game_state):
   
    result = GetBestMove(game_state,-1, depth,0)
  #  print result[0]
    return result[0]
















def drawCircleArc(gameDisplay, color, node1, node2):

    center = (int((node1.center[0] + node2.center[0])/2), int((node1.center[1] + node2.center[1])/2))
    distance = math.sqrt((node2.center[0] - node1.center[0])**2 + (node2.center[1] - node1.center[1])**2)
    radius = int(distance/2)
    (x,y) = center
    rect = (x-radius, y-radius, radius*2, radius*2)
    startRad = 2*math.pi - np.arctan2(node1.center[1] - node2.center[1], node1.center[0] - node2.center[0])
    endRad = startRad + math.pi
   
    pygame.draw.arc(gameDisplay, color, rect, startRad, endRad)

def draw(gameDisplay, nodes):

    for i in range(len(nodes)):
        pygame.draw.circle(gameDisplay, nodes[i].color, nodes[i].center, nodes[i].radius)
        font = pygame.font.SysFont('Comic Sans MS', int(nodes[i].radius*1.5))
        text = font.render(str(nodes[i].no), False, BLACK)
        gameDisplay.blit(text, nodes[i].center)

        links = nodes[i].link
        for j in range(i+1, len(nodes)):
            if nodes[j].no in links:
                drawCircleArc(gameDisplay, BLACK, nodes[i], nodes[j])
                #pygame.draw.line(gameDisplay, BLACK, nodes[i].center, nodes[j].center)

def generate_nodes(number_of_nodes, maxx, maxy, radius):

    nodes = []
    for i in range(number_of_nodes):
        varx=random.randint(0,maxx-radius)
        vary=random.randint(0,maxy-radius)
        center = (random.randint(varx, maxx - radius), random.randint(vary, maxy - radius))
        nodes.append(node(i, RED, center, radius, []))

    return nodes

def get_moves(nodes):

    moves = []
    for i in range(len(nodes)):
        if not len(nodes[i].link) == 3:
            for j in range(i, len(nodes)):
                if not len(nodes[j]).link == 3:
                    moves.append((nodes[i].no, nodes[j].no))

    return moves

def generate_new_node(index, color, node1, node2, radius):

    center = (int((node1.center[0] + node2.center[0])/2), int((node1.center[1] + node2.center[1])/2))
    distance = math.sqrt((node2.center[0] - node1.center[0])**2 + (node2.center[1] - node1.center[1])**2)
    radii = int(distance/2)

    mult = random.randint(1, 10)
    radii = int(mult*float(radii/10))

    x_or_y = random.randint(0, 1)
    add_or_sub = random.randint(0, 1)
    if radii == 0:
        radii = 5*radius
    if x_or_y == 0:
        if add_or_sub == 0:
            center = (center[0] + radii, center[1])
        elif add_or_sub == 1:
            center = (center[0] - radii, center[1])
    elif x_or_y == 1:
        if add_or_sub == 0:
            center = (center[0], center[1] + radii)
        elif add_or_sub == 1:
            center = (center[0], center[1] - radii)

    new_node = node(index, color, center, radius, [node1, node2])

    return new_node

if __name__=="__main__":


    pygame.init()
    pygame.font.init()

    height = 800
    width = 600
    gameDisplay = pygame.display.set_mode((height, width))
    pygame.display.set_caption("Game of Sprouts")

    init_n = input("Enter the number of initial nodes: ")
    depth = input("Enter depth: ")    
    n=init_n
    g=np.zeros((n,n))
    g=g.astype(int)
    game_state=g.tolist()
    
    nodes = generate_nodes(int(init_n), height, width, 15)

    gameexit = False

    player1 = player(BLUE, True)
    player2 = player(GREEN, False)

    while not gameexit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameexit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    if isTerminalState(game_state)==1:
                        if player1.turn:
                            print("Player1 loses and Player2 wins")
                        elif player2.turn:
                            print("Player2 loses and Player1 wins") 
                        gameexit=True 
                        break                          
                    clr = ()
                    if player1.turn:
                        print("Its player1's turn to play")
                        print("Enter what nodes to connect:")
                        clr = player1.color
                        node1 = input()
                        node2 = input()
                        game_state=GetNewGameState(game_state,(node1+1, node2+1))
                        
                        
                        if len(nodes[int(node1)].link) == 3 or len(nodes[int(node2)].link) == 3:
                            print("Invalid move!")
                        else:
                            player2.moves.append([int(node1), int(node2)])
                            new_node = generate_new_node(len(nodes), clr, nodes[int(node1)], nodes[int(node2)], 15)
                            nodes[int(node1)].link.append(new_node.no)
                            nodes[int(node2)].link.append(new_node.no)
                            nodes.append(generate_new_node(len(nodes), clr, nodes[int(node1)], nodes[int(node2)], 15))
                            player1.turn = False
                            player2.turn = True
                            print("Done!")
                    elif player2.turn:
                        print("Its player2's turn to play")
                        print("Enter what nodes to connect:")
                        clr = player2.color
                        node1, node2 = GetMove(game_state)
                        node1=node1-1
                        node2=node2-1
                        print (node1,node2)
                        game_state=GetNewGameState(game_state,(node1+1, node2+1))
                        
                  #      print(nodes[int(node1)].no)
                        if len(nodes[int(node1)].link) == 3 or len(nodes[int(node2)].link) == 3:
                            print("Invalid move!")
                        else:
                            player2.moves.append([int(node1), int(node2)])
                            new_node = generate_new_node(len(nodes), clr, nodes[int(node1)], nodes[int(node2)], 15)
                            nodes[int(node1)].link.append(new_node.no)
                            nodes[int(node2)].link.append(new_node.no)
                            nodes.append(generate_new_node(len(nodes), clr, nodes[int(node1)], nodes[int(node2)], 15))
                            player1.turn = True
                            player2.turn = False
                            print("Done!")

        gameDisplay.fill(WHITE)
        draw(gameDisplay, nodes)

        pygame.display.update()

    pygame.quit()
