import pygame
import math
import numpy as np
import random

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
        center = (random.randint(0, maxx - radius), random.randint(0, maxy - radius))
        nodes.append(node(i, RED, center, radius, []))

    return nodes

def get_moves(nodes):

    moves = []
    for i in range(len(nodes)):
        if not len(nodes[i].link) == 3:
            for j in range(i, len(nodes)):
                if not len(nodes[j]).link == 3
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
                    clr = ()
                    if player1.turn:
                        print("Its player1's turn to play")
                        print("Enter what nodes to connect:")
                        clr = player1.color
                        node1 = input()
                        node2 = input()
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
                        node1 = input()
                        node2 = input()
                        print(nodes[int(node1)].no)
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
