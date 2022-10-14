import os 
import pygame
import socket
import time
import threading 
from decoder import decoder , encoder



NICKNAME = input('Enter Your Nickname : \n')
HOST='127.0.0.1'
PORT = 1234
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((socket.gethostname()  ,PORT)) 





GAME_WIDTH  = 300
GAME_HEIGHT  = 300
WHITE_COLOR = (255,255,255)
BLACK_COLOR = (0,0,0)
RED_COLOR = (255,0,0)
GREEN_COLOR = (0,255,0)
LETTER_X= pygame.image.load(os.path.join('images', 'letterX.jpg'))
LETTER_O= pygame.image.load(os.path.join('images', 'letterO.jpg'))
LETTER_X = pygame.transform.scale(LETTER_X, (100, 100))
LETTER_O = pygame.transform.scale(LETTER_O, (100, 100))

gameWindow = pygame.display.set_mode((GAME_WIDTH,GAME_HEIGHT))
pygame.display.set_caption('TicTacToe')

def string_adder(x,y,z):
    return str(x)+str(y)+str(z)
 

class Grid:
    def __init__(self):
        
        self.grid_lines  = [[(GAME_WIDTH/3 ,0),(GAME_WIDTH/3 ,GAME_HEIGHT)] , 
                            [(GAME_WIDTH*2/3 ,0),(GAME_WIDTH*2/3 ,GAME_HEIGHT)] , 
                            [(0 ,GAME_HEIGHT/3),(GAME_WIDTH ,GAME_HEIGHT/3)] , 
                            [(0 ,GAME_HEIGHT*2/3),(GAME_WIDTH ,GAME_HEIGHT*2/3)] ]
        self.grid = [[0 for _ in range(3)] for _ in range(3)]
        self.current_player = 0
        self.turn_over = 0


    def print_grid(self):
        for g in self.grid:
            print(g)

    def draw(self ,gameWindow):
        for line in self.grid_lines:
            pygame.draw.line(gameWindow , WHITE_COLOR   , line[0] ,line[1] ,4)
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j]=='X':
                    gameWindow.blit(LETTER_X ,(100*j,100*i))
                if self.grid[i][j]=='O':
                    gameWindow.blit(LETTER_O ,(100*j,100*i))

    def get_cell_value(self ,  x, y):
        return self.grid[y][x]
    def set_cell_value(self   , x , y , value):        
        self.grid[y][x] = value
    def reset_grid(self):
        self.grid = [[0 for _ in range(3)] for _ in range(3)]
        self.current_player = 0

        
    def click_mouse(self , x,y ,player):
        if self.grid[y][x]==0:
            self.set_cell_value(x,y,player)
            self.current_player = (self.current_player+1)%2
             

    def is_grid_full(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 0:
                    return False
        return True
    def winner_checker(self):
        p = self.grid
        if string_adder(p[0][0],p[0][1],p[0][2])=='XXX':
            return 'X'
        if string_adder(p[1][0],p[1][1],p[1][2])=='XXX':
            return 'X'
        if string_adder(p[2][0],p[2][1],p[2][2])=='XXX':
            return 'X'
        if string_adder(p[0][0],p[1][0],p[2][0])=='XXX':
            return 'X'
        if string_adder(p[0][1],p[1][1],p[2][1])=='XXX':
            return 'X'
        if string_adder(p[0][2],p[1][2],p[2][2])=='XXX':
            return 'X'
        if string_adder(p[0][0],p[1][1],p[2][2])=='XXX':
            return 'X'
        if string_adder(p[2][0],p[1][1],p[0][2])=='XXX':
            return 'X'


        if string_adder(p[0][0],p[0][1],p[0][2])=='OOO':
            return 'O'
        if string_adder(p[1][0],p[1][1],p[1][2])=='OOO':
            return 'O'
        if string_adder(p[2][0],p[2][1],p[2][2])=='OOO':
            return 'O'
        if string_adder(p[0][0],p[1][0],p[2][0])=='OOO':
            return 'O'
        if string_adder(p[0][1],p[1][1],p[2][1])=='OOO':
            return 'O'
        if string_adder(p[0][2],p[1][2],p[2][2])=='OOO':
            return 'O'
        if string_adder(p[0][0],p[1][1],p[2][2])=='OOO':
            return 'O'
        if string_adder(p[2][0],p[1][1],p[0][2])=='OOO':
            return 'O'
        return -1
        
        
    
        



grid = Grid()

def message_reciever_sender():
    global grid
    while True:
        try:
            msg = decoder(client.recv(1024))
            if msg =='welcome':
                client.send(encoder(NICKNAME))
            else:
                grid = msg 
                pass
        except:
            print('Error Occured !')
            #client.close()
            break




#keeps the function running
t = threading.Thread(target=message_reciever_sender)
t.start()






running  = True


while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running  = False
            break
        if event.type ==pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                x = int(pos[0]/100)
                y = int(pos[1]/100)
                print(x,y)
                

                if grid.turn_over==0: 
                    if grid.current_player==0: 
                        grid.click_mouse(x,y,'X')
                    if grid.current_player==1: 
                        grid.click_mouse(x,y,'O')
                    client.send(encoder(grid))
                    grid.turn_over = 1

                winner = grid.winner_checker()
                if winner!=-1:
                    print(winner  +  str(' wins!!'))
                    gameWindow.fill((0,0, 0))
                    grid.draw(gameWindow)
                    pygame.display.update()
                    time.sleep(1)
                    grid.reset_grid()
                    client.send(encoder(grid))
                if grid.is_grid_full():
                    gameWindow.fill((0,0, 0))
                    grid.draw(gameWindow)
                    pygame.display.update()
                    time.sleep(1)
                    grid.reset_grid()
                    client.send(encoder(grid))
                
                
                



    gameWindow.fill((0,0, 0))
    grid.draw(gameWindow)
    pygame.display.update()






