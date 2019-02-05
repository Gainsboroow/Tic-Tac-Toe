"""
Tic Tac Toe
Made by Gainsboroow 
Github : https://github.com/Gainsboroow/
Github repository : https://github.com/Gainsboroow/Tic-Tac-Toe
Play Tic Tac Toe versus a bot using a MinMax Algorithm.
1 chance out of 2 to be the first to start playing.
"""

from sys import setrecursionlimit
from copy import deepcopy
from random import *
import pygame
from pygame.locals import *

setrecursionlimit(10**6)

pygame.init()
size = width, height = 300, 300
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tic Tac Toe")

caseSize = 100
grid = [ [-1 for i in range(3)] for a in range(3) ]
for i in range(caseSize, caseSize*3, caseSize):
    pygame.draw.line(screen, (255,255,255), (i,0), (i,height), 5)
    pygame.draw.line(screen, (255,255,255), (0, i), (width,i), 5)

pygame.display.flip()

joueur = 0
tourBot = randint(0,1)

def check(grid, traceGagnant = True):
    for line in range(3):
        threeInARow = True
        for col in range(1, 3):
            if grid[line][col-1] != grid[line][col]:
                threeInARow = False
                break
        if grid[line][0] != -1 and threeInARow:
            if traceGagnant:
                pygame.draw.line(screen, (255,255,255), (10, line*caseSize+caseSize//2), (width-10, line*caseSize+caseSize//2), 4)
            return grid[line][0]
    
    for col in range(3):
        threeInARow = True
        for line in range(1,3):
            if grid[line][col] != grid[line-1][col]:
                threeInARow = False
                break
        if grid[0][col] != -1 and threeInARow:
            if traceGagnant:
                pygame.draw.line(screen, (255,255,255), (col*caseSize+caseSize//2, 10), (col*caseSize+caseSize//2, height-10), 4)
            return grid[0][col]

    threeInARow = True
    for i in range(1, 3):
        if grid[i][i] != grid[i-1][i-1]:
            threeInARow = False

    if grid[0][0] != -1 and threeInARow:
        if traceGagnant:
            pygame.draw.line(screen, (255,255,255), (10, 10), (width - 10, height - 10), 4)
        return grid[0][0]

    threeInARow = True
    for i in range(3):
        try:
            if grid[2-i][i] != grid[1-i][i+1]:
                threeInARow = False
                break
        except : 
            pass
                
    if grid[2][0] != -1 and threeInARow:
        if traceGagnant:
            pygame.draw.line(screen, (255,255,255), (width - 10, 10), (10, height - 10), 4)
        return grid[2][0]

    fullGrid = not(any([-1 in grid[i] for i in range(3)]))
    if fullGrid:
        return 3

    return -1

def cacherAncien(x,y):
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(x*caseSize+5,y*caseSize+5,caseSize-10, caseSize-10))

def dessiner(caseX, caseY, colorRatio = 1):
    centerX = caseSize // 2 + caseX * caseSize
    centerY = caseSize // 2 + caseY * caseSize
    if not(joueur): #J1
        pt1, pt2 = (centerX-caseSize//2+10, centerY-caseSize//2+10), (centerX+caseSize//2-10, centerY+caseSize//2-10)
        pt3, pt4 = (centerX-caseSize//2+10, centerY+caseSize//2-10), (centerX+caseSize//2-10, centerY-caseSize//2+10)
        pygame.draw.line(screen, (255//colorRatio,0,0), pt1, pt2, 10)
        pygame.draw.line(screen, (255//colorRatio,0,0), pt3, pt4, 10)
    else: #J2          
        pygame.draw.circle(screen, (0,255//colorRatio,255//colorRatio), (centerX, centerY), caseSize//2 - 10, 5)
        pygame.display.flip()


def minMax(grid, player):
    winner = check(grid, False)

    if winner == 3:
        return 0, (0,0)
    elif winner == tourBot:
        return 10, (0,0)
    elif winner == 1 - tourBot:
        return -10, (0,0)

    copyGrid = deepcopy(grid)
    
    nextMove = -1,-1

    if player != tourBot: #Humain, Minimiser le score
        score = float("inf")
        for lig in range(3):
            for col in range(3):
                if copyGrid[lig][col] == -1:
                    copyGrid[lig][col] = player 
                    temp, _ = minMax(deepcopy(copyGrid), 1 - player)
                    copyGrid[lig][col] = -1
                    if temp == -10:
                        return temp, (lig,col)
                    elif temp < score:
                        score = temp 
                        nextMove = lig, col

    else: #Machine, Maximiser le score
        score = -float("inf")
        for lig in range(3):
            for col in range(3):
                if copyGrid[lig][col] == -1:
                    copyGrid[lig][col] = player 
                    temp, _ = minMax(deepcopy(copyGrid), 1 - player)
                    copyGrid[lig][col] = -1
                    if temp == 10:
                        return temp, (lig,col)
                    elif temp > score:
                        score = temp 
                        nextMove = lig, col

    return score, nextMove

precCaseX, precCaseY = -1, -1
endGame = False 

while 1:
    if joueur != tourBot:
        x,y = pygame.mouse.get_pos()
        caseX = x // caseSize
        caseY = y // caseSize  

        if grid[caseY][caseX] == -1:
            dessiner(caseX, caseY, 2)

        if (precCaseX, precCaseY) != (caseX, caseY) and grid[precCaseY][precCaseX] == -1:
            cacherAncien(precCaseX,precCaseY)
        precCaseX, precCaseY = caseX, caseY 

        for event in pygame.event.get():
            if event.type == QUIT: 
                exit()
            elif event.type == MOUSEBUTTONDOWN and not(endGame): 
                if grid[caseY][caseX] != -1:
                    continue

                dessiner(caseX, caseY)
                grid[caseY][caseX] = joueur

                gagnant = check(grid)
                if gagnant == 3:
                    print('Match nul')
                    endGame = True 

                elif gagnant != -1:
                    print("Joueur", gagnant + 1, "a gagné !")
                    endGame = True
        
                joueur = 1 - joueur
        
    else:
        score, nextMove = minMax(grid, joueur)

        dessiner(nextMove[1], nextMove[0])
        grid[nextMove[0]][nextMove[1]] = joueur

        gagnant = check(grid)
        if gagnant == 3:
            print('Match nul')
            endGame = True 

        elif gagnant != -1:
            print("Joueur", gagnant + 1, "a gagné !")
            endGame = True

        joueur = 1 - joueur
    
    pygame.display.flip()

    
