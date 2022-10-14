import os 
import pygame
import socket
import time
import threading
from decoder import decoder , encoder
 
 

HOST='127.0.0.1'
PORT = 1234
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostname() ,PORT))
server.listen(2)

CLIENT_ARRAY = []
NICKNAMES_ARRAY = []
SCORE_ARRAY = [] 





 


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

 

def string_adder(x,y,z):
    return str(x)+str(y)+str(z)

 

class Grid:
    def __init__(self):
        
        self.grid_lines  = [[(GAME_WIDTH/3 ,0),(GAME_WIDTH/3 ,GAME_HEIGHT)] , 
                            [(GAME_WIDTH*2/3 ,0),(GAME_WIDTH*2/3 ,GAME_HEIGHT)] , 
                            [(0 ,GAME_HEIGHT/3),(GAME_WIDTH ,GAME_HEIGHT/3)] , 
                            [(0 ,GAME_HEIGHT*2/3),(GAME_WIDTH ,GAME_HEIGHT*2/3)] ]
        self.grid = [[0 for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
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




def broadcast_message(message):
    for c in CLIENT_ARRAY: 
        c.send(encoder(message))

def message_listener(client):
    while True:
        try:
            msg = decoder(client.recv(1024))
            print(msg)
            broadcast_message(msg)
        except:
            index = CLIENT_ARRAY.index(client)
            score = SCORE_ARRAY[index]
            CLIENT_ARRAY.remove(client)
            SCORE_ARRAY.remove(score)
            client.close()
            break

def connection_acceptor():
    while True:
        print('Server Listening...')
        client  , addr = server.accept()
        client.send(encoder('welcome'))
        nickname = decoder(client.recv(1024))
        print('connection made at : {} '.format(nickname) ,  addr )
        CLIENT_ARRAY.append(client)
        NICKNAMES_ARRAY.append(nickname)
        SCORE_ARRAY.append(0)
        t = threading.Thread(target = message_listener ,args=[client])
        t.start()


connection_acceptor()
   

    