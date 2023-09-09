import pygame
import numpy as np
import math
pygame.init()
n = 6
m = 7
# n = int(input('Enter n (number of rows): '))
# m = int(input('Enter m (number of columns): '))

#! In hard mode, the algorithm of choice is Minimax, whereas in easy mode, a greedy algorithm is employed

WIDTH, HEIGHT = m*100,n*100 
WIN = pygame.display.set_mode((WIDTH,HEIGHT)) 
FPS = 60
pygame.display.set_caption("Connect 4")
WHITE = (255,255,255)
BACKGROUND = (13,17,23)
RED = (255,0,0)
BLUE = (0,0,255)
ORANGE = (255,166,75)
GREY = (150,150,150)
DARK_GREY = (100,100,100)
# TURN = 1 # 1 for first player RED. 2 for second player BLUE must be  random. 3 when game is finished WHILTE
# In playing with ai , first player is you and second player is ai
TURN = np.random.randint(1,3)
TURN = 1
# TEXT_TO_SHOW = "player one"
TEXT_TO_SHOW = "Select game mode "
IS_GAME_START = False
matrix_of_game = np.zeros((n,m))
MOD = ""
def reset():
    global TEXT_TO_SHOW
    global IS_GAME_START
    global matrix_of_game
    global MOD
    MOD = ""
    IS_GAME_START = False
    global TURN
    TEXT_TO_SHOW = "Select game mode"
    matrix_of_game = np.zeros((n,m))
    # TURN = 1 # 1 for first player RED. 2 for second player BLUE must be  random. 3 when game is finished WHILTE
    TURN = np.random.randint(1,3)
def text_objects(text, font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()
def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(WIN, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(WIN, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    WIN.blit(textSurf, textRect) 
def is_full(matrix):
    for i in range(n):
        for j in range(m):
            if matrix[i,j] == 0: return False
    return True
def change_turn():
    global TURN
    if TURN == 1:TURN = 2
    elif TURN == 2:TURN = 1
def draw_matrix():
    pygame.draw.rect(WIN,BACKGROUND,(0,0,WIDTH,2*HEIGHT/(n+3)))
    if TURN == 1: color = RED
    elif TURN == 2:  color = BLUE
    else:  color = BACKGROUND
    if MOD == 'pvp' or ("pva" in MOD and TURN == 1):
        pygame.draw.circle(WIN,color,(pygame.mouse.get_pos()[0], HEIGHT/(n+3)),math.sqrt((WIDTH*HEIGHT)/ (10*((m*n)))),width=0)
    if 'win' in TEXT_TO_SHOW:
        button("Back",WIDTH/2 - 50 ,HEIGHT/(n+3),100,50,GREY,DARK_GREY,reset)
    for i in range(n):
        for j in range(m):
            if matrix_of_game[i,j]==0:
                color = BACKGROUND
            elif matrix_of_game[i,j]==1:
                color = RED
            else:
                color = BLUE
            pygame.draw.circle(WIN,color,(WIDTH/(m+1) * (j+1), HEIGHT/(n+3)*(i+3)),math.sqrt((WIDTH*HEIGHT)/ (10*((m*n)))),width=0)
def check_wining(matrix,player):
    wininning_state = np.array((player,player,player,player))
    #check vertically
    for i in range(n-3):
        for j in range(m):
            if all (matrix[i:i+4,j] == wininning_state):return True
    #check horizontally
    for i in range(n):
        for j in range(m-3):
            if all (matrix[i,j:j+4] == wininning_state):return True  
    # check diagonal (main) 
    for i in range(n-3):
        for j in range(m-3):
            if all ([matrix[i+k,j+k] == wininning_state[k] for k in range(4)]):return True
    # check diagonal (minor) 
    for i in range(3,n):
        for j in range(m-3):
            if all ([matrix[i-k,j+k] == wininning_state[k] for k in range(4)]):return True
    return False
def check_add_dot(index):
    global TEXT_TO_SHOW
    global TURN
    if matrix_of_game[0,index] != 0:
        TEXT_TO_SHOW = "Chooser another place!!!"
        return False
    return True
def add_dot(matrix,index,player):
    global TEXT_TO_SHOW
    global TURN
    for i in range (n):
        if matrix[n-1-i,index] == 0:
            matrix[n-1-i,index]=player
            return i
def pressed_mouse():
    global TEXT_TO_SHOW
    global TURN
    if 'win' in TEXT_TO_SHOW:
        return
    for j in range(m+2):
        if  pygame.mouse.get_pos()[0]<(((WIDTH/(m+1) * (j+1))+(WIDTH/(m+1) * (j)))/2): #pygame.mouse.get_pos()[0]>(WIDTH/(m) * (j)) and
            go_to = j 
            break
    go_to -= 1
    if go_to == -1 :go_to = 0
    if go_to == m+1 or go_to == m :go_to = m-1
    if not check_add_dot(go_to): return
    add_dot(matrix_of_game,go_to,TURN)
    if check_wining(matrix_of_game,TURN):
        if TURN == 1: TEXT_TO_SHOW = "player one win!!"
        if TURN == 2: TEXT_TO_SHOW = "player two win!!" 
        TURN = 3
        return
    if  is_full(matrix_of_game):
        TURN = 3
        TEXT_TO_SHOW = "No winner!!"
        return
    change_turn()
    if MOD == "pvp":
        if TURN == 1: TEXT_TO_SHOW = "player one"
        if TURN == 2: TEXT_TO_SHOW = "player two" 
    if "pva" in MOD:
        if TURN == 1:
            TEXT_TO_SHOW = "player one (you)"
        if TURN == 2:
            TEXT_TO_SHOW = "player two (AI)" 
            WIN.fill(ORANGE)
            draw_matrix()
            smallText = pygame.font.SysFont("comicsansms",20)
            textSurf, textRect = text_objects(TEXT_TO_SHOW, smallText)
            textRect.center = ( (WIDTH/2), (20)) 
            WIN.blit(textSurf, textRect) 
            pygame.display.update()
            pygame.time.wait(700)
            if MOD == 'pvaminmax':
                AI_choose_minmax(2)
            if MOD == 'pvagreedy':
                AI_choose_greedy(2)
def player_vs_player():
    global TEXT_TO_SHOW
    global IS_GAME_START
    global MOD
    if TURN == 1: TEXT_TO_SHOW = "player one"
    if TURN == 2: TEXT_TO_SHOW = "player two" 
    IS_GAME_START = True
    MOD = 'pvp'
def count(array,value):
    res = 0
    for i in array:
        if i == value:
            res += 1
    return res
def calculate_score_4_list(check_list,agent): 
    opponent = 1
    if agent == 1 :opponent = 2
    if count(check_list,agent) == 4: return 100
    if count(check_list,agent) == 3 and count(check_list,0) == 1: return 5
    if count(check_list,agent) == 2 and count(check_list,0) == 2: return 2
    if count(check_list,opponent) == 3 and count(check_list,0) == 1: return -10
    return 0
def calculate_scroe_state_greedy(matrix,agent):
    # calculate score for matrix
    #similar to calculate_scroe_state but check that the row exist that opponent have 2 value in middle of 6 house that 4 other house is empty 
    opponent = 1
    if agent == 1 :opponent = 2
    score = 0
    center_array = [i for i in list(matrix[:, m//2])]
    center_count = count(center_array,agent)
    score += center_count * 3

    #check vertically
    for i in range(n-3):
        for j in range(m):
            score += calculate_score_4_list (matrix[i:i+4,j] ,agent)
    #check horizontally
    for i in range(n):
        for j in range(m-3):
            score += calculate_score_4_list (matrix[i,j:j+4] ,agent)
    # for i in range(n):
    for j in range(m-5):
        if all (matrix[n-1,j:j+6] == [0,0,opponent,opponent,0,0]):
            score += -40
    # check diagonal (main) 
    for i in range(n-3):
        for j in range(m-3):
            score += calculate_score_4_list ([matrix[i+k,j+k]  for k in range(4)],agent)
    # check diagonal (minor) 
    for i in range(3,n):
        for j in range(m-3):
            score += calculate_score_4_list ([matrix[i-k,j+k] for k in range(4)],agent)
    return score
def calculate_scroe_state(matrix,agent):
    # calculate score for matrix
    score = 0
    center_array = [i for i in list(matrix[:, m//2])]
    center_count = count(center_array,agent)
    score += center_count * 3

    #check vertically
    for i in range(n-3):
        for j in range(m):
            score += calculate_score_4_list (matrix[i:i+4,j] ,agent)
    #check horizontally
    for i in range(n):
        for j in range(m-3):
            score += calculate_score_4_list (matrix[i,j:j+4] ,agent)
    # check diagonal (main) 
    for i in range(n-3):
        for j in range(m-3):
            score += calculate_score_4_list ([matrix[i+k,j+k]  for k in range(4)],agent)
    # check diagonal (minor) 
    for i in range(3,n):
        for j in range(m-3):
            score += calculate_score_4_list ([matrix[i-k,j+k] for k in range(4)],agent)
    return score
def minimax(alpha,beta,matrix,depth,player,is_max_or_min):
    opponent = 1
    if player == 1 :opponent = 2
    if check_wining(matrix,player) :
        return (None, 10000000)
    if check_wining(matrix,opponent) :
        return (None, -10000000)
    if is_full(matrix) :return (None , 0)
    if depth == 0: return (None, calculate_scroe_state(matrix,player))
    locations = []
    for i in range(m):
        if check_add_dot(i):locations.append(i)
    if is_max_or_min == 'max': 
        value = -math.inf
        choose = np.random.choice(locations)
        for loc in locations:
            tmp_matrix = matrix.copy()
            add_dot(tmp_matrix,loc,player)
            new_score = minimax(alpha,beta,tmp_matrix, depth-1,player,'min')[1]
            if new_score > value:
                value = new_score
                choose = loc
            alpha = max(alpha, value)
            if alpha >= beta:
                # beta pruning
                break
        return choose,value
    if is_max_or_min == 'min': 
        value = math.inf
        choose = np.random.choice(locations)
        for loc in locations:
            tmp_matrix = matrix.copy()
            add_dot(tmp_matrix,loc,opponent)
            new_score = minimax(alpha,beta,tmp_matrix, depth-1,player,'max')[1]
            if new_score < value:
                value = new_score
                choose = loc
            beta = min(beta, value)
            if alpha >= beta:
                # alpha pruning
                break
        return choose,value
def AI_choose_greedy(agent):
    global TEXT_TO_SHOW
    global TURN
    locations = []#list of locatins that ai can put
    for i in range(m):
        if check_add_dot(i):locations.append(i)
    score = -10000000
    action = 0
    for i in locations:
        temp_matrix = matrix_of_game.copy()
        add_dot(temp_matrix,i,TURN)
        if score < calculate_scroe_state_greedy(temp_matrix,agent):
            score = calculate_scroe_state_greedy(temp_matrix,agent)
            action = i
    add_dot(matrix_of_game,action,agent)
    if check_wining(matrix_of_game,TURN):
        if TURN == 1: TEXT_TO_SHOW = "player one win!!"
        if TURN == 2: TEXT_TO_SHOW = "player two win!!" 
        TURN = 3
        return
    if is_full(matrix_of_game):
        TURN = 3
        TEXT_TO_SHOW = "No winner!!"
        return
    change_turn()
    if "pva" in MOD:
        if TURN == 1:
            TEXT_TO_SHOW = "player one (you)"
        if TURN == 2:
            TEXT_TO_SHOW = "player two (AI)" 
    if  "ava" in MOD:
        if TURN == 1:
            TEXT_TO_SHOW = "player two (AI_1)" 
        if TURN == 2:
            TEXT_TO_SHOW = "player two (AI_2)" 
def AI_choose_minmax(agent):
    global TEXT_TO_SHOW
    global TURN
    choose,score = minimax(-math.inf,math.inf,matrix_of_game,3,agent,'max')
    add_dot(matrix_of_game,choose,TURN)
    if check_wining(matrix_of_game,TURN):
        if TURN == 1: TEXT_TO_SHOW = "player one win!!"
        if TURN == 2: TEXT_TO_SHOW = "player two win!!" 
        TURN = 3
        return
    if is_full(matrix_of_game):
        TURN = 3
        TEXT_TO_SHOW = "No winner!!"
        return
    change_turn()
    if "pva"in MOD:
        if TURN == 1:
            TEXT_TO_SHOW = "player one (you)"
        if TURN == 2:
            TEXT_TO_SHOW = "player two (AI)" 
    if "ava" in MOD:
        if TURN == 1:
            TEXT_TO_SHOW = "player two (AI_1)" 
        if TURN == 2:
            TEXT_TO_SHOW = "player two (AI_2)" 
def player_vs_AI_minmax():
    global TEXT_TO_SHOW
    global IS_GAME_START
    global MOD
    IS_GAME_START = True
    MOD = 'pvaminmax'
    if TURN == 1: 
        TEXT_TO_SHOW = "player one (you)"
    if TURN == 2: 
        TEXT_TO_SHOW = "player two (AI)" 
        WIN.fill(ORANGE)
        draw_matrix()
        smallText = pygame.font.SysFont("comicsansms",20)
        textSurf, textRect = text_objects(TEXT_TO_SHOW, smallText)
        textRect.center = ( (WIDTH/2), (20)) 
        WIN.blit(textSurf, textRect) 
        pygame.display.update()
        pygame.time.wait(700)
        AI_choose_minmax(2)
def AI_vs_AI_minmax():
    global TEXT_TO_SHOW
    global IS_GAME_START
    global MOD
    IS_GAME_START = True
    MOD = "avaminmax"
    next_block_move_time = 0
    while True:
        if TURN == 1: 
            TEXT_TO_SHOW = "player one (AI_1)"
            WIN.fill(ORANGE)
            draw_matrix()
            smallText = pygame.font.SysFont("comicsansms",20)
            textSurf, textRect = text_objects(TEXT_TO_SHOW, smallText)
            textRect.center = ( (WIDTH/2), (20)) 
            WIN.blit(textSurf, textRect) 
            current_time = pygame.time.get_ticks() 
            if current_time > next_block_move_time:
                next_block_move_time = current_time + 100
                pygame.display.update()
                AI_choose_minmax(1)
        if TURN == 2: 
            TEXT_TO_SHOW = "player two (AI_2)" 
            WIN.fill(ORANGE)
            draw_matrix()
            smallText = pygame.font.SysFont("comicsansms",20)
            textSurf, textRect = text_objects(TEXT_TO_SHOW, smallText)
            textRect.center = ( (WIDTH/2), (20)) 
            WIN.blit(textSurf, textRect) 
            current_time = pygame.time.get_ticks() 
            if current_time > next_block_move_time:
                next_block_move_time = current_time + 100
                pygame.display.update()
                AI_choose_minmax(2)
        if TURN == 3:
            break
def player_vs_AI_greedy():
    global TEXT_TO_SHOW
    global IS_GAME_START
    global MOD
    IS_GAME_START = True
    MOD = 'pvagreedy'
    if TURN == 1: 
        TEXT_TO_SHOW = "player one (you)"
    if TURN == 2: 
        TEXT_TO_SHOW = "player two (AI)" 
        WIN.fill(ORANGE)
        draw_matrix()
        smallText = pygame.font.SysFont("comicsansms",20)
        textSurf, textRect = text_objects(TEXT_TO_SHOW, smallText)
        textRect.center = ( (WIDTH/2), (20)) 
        WIN.blit(textSurf, textRect) 
        pygame.display.update()
        pygame.time.wait(700)
        AI_choose_greedy(2)
def AI_vs_AI_greedy():
    global TEXT_TO_SHOW
    global IS_GAME_START
    global MOD
    IS_GAME_START = True
    MOD = "avagreedy"
    next_block_move_time = 0
    while True:
        if TURN == 1: 
            TEXT_TO_SHOW = "player one (AI_1)"
            WIN.fill(ORANGE)
            draw_matrix()
            smallText = pygame.font.SysFont("comicsansms",20)
            textSurf, textRect = text_objects(TEXT_TO_SHOW, smallText)
            textRect.center = ( (WIDTH/2), (20)) 
            WIN.blit(textSurf, textRect) 
            current_time = pygame.time.get_ticks() 
            if current_time > next_block_move_time:
                next_block_move_time = current_time + 100
                pygame.display.update()
                AI_choose_greedy(1)
        if TURN == 2: 
            TEXT_TO_SHOW = "player two (AI_2)" 
            WIN.fill(ORANGE)
            draw_matrix()
            smallText = pygame.font.SysFont("comicsansms",20)
            textSurf, textRect = text_objects(TEXT_TO_SHOW, smallText)
            textRect.center = ( (WIDTH/2), (20)) 
            WIN.blit(textSurf, textRect) 
            current_time = pygame.time.get_ticks() 
            if current_time > next_block_move_time:
                next_block_move_time = current_time + 100
                pygame.display.update()
                AI_choose_greedy(2)
        if TURN == 3:
            break
def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        WIN.fill(BACKGROUND)
        if IS_GAME_START:
            WIN.fill(ORANGE)
            draw_matrix()
        else:
            button("Player vs Player",WIDTH/2 - 110 ,HEIGHT/4,220,50,GREY,DARK_GREY,player_vs_player)
            button("Player vs AI (Hard)",WIDTH/2 - 225 ,HEIGHT/4 + 80,220,50,GREY,DARK_GREY,player_vs_AI_minmax)
            button("Player vs AI (Easy)",WIDTH/2  + 5 ,HEIGHT/4 + 80,220,50,GREY,DARK_GREY,player_vs_AI_greedy)
            button("AI vs AI (Hard)",WIDTH/2 - 225 ,HEIGHT/4 + 160,220,50,GREY,DARK_GREY,AI_vs_AI_minmax)
            button("AI vs AI (Easy)",WIDTH/2 + 5 ,HEIGHT/4 + 160,220,50,GREY,DARK_GREY,AI_vs_AI_greedy)
            button("Exit",WIDTH/2 - 110 ,HEIGHT/4 + 240,220,50,GREY,DARK_GREY,exit)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN :
                if IS_GAME_START and (MOD == "pvp" or ("pva" in MOD and TURN == 1)) :
                    if pygame.mouse.get_pressed()[0]:
                        pressed_mouse()
        if TEXT_TO_SHOW != "":
            smallText = pygame.font.SysFont("comicsansms",20)
            textSurf, textRect = text_objects(TEXT_TO_SHOW, smallText)
            textRect.center = ( (WIDTH/2), (20)) 
            WIN.blit(textSurf, textRect) 
        if MOD == "":
            smallText = pygame.font.SysFont("comicsansms",15)
            textSurf, textRect = text_objects("Connect 4", smallText)
            textRect.center = ( (len("Connect 4")*4), (10)) 
            WIN.blit(textSurf, textRect) 
        pygame.display.update()
    pygame.quit()
if __name__=="__main__":
    main() 