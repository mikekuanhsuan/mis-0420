import pygame
import time
import random
 

# 初始化 Pygame
pygame.init()
 
# 定義顏色常數
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
 
# 設定遊戲顯示視窗的大小
dis_width = 600
dis_height = 400
 
# 創建遊戲顯示視窗並設置標題
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by Edureka')
 
# 設置遊戲時鐘
clock = pygame.time.Clock()
 
# 設定貪食蛇方塊的大小和速度
snake_block = 10
snake_speed = 20
 
# 定義用於顯示得分和消息的字型
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
 

# 函數：顯示得分
def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])
 
 
# 函數：繪製貪食蛇
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])
 
# 函數：顯示消息
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])
 

# 主遊戲循環函數
def gameLoop():
    # 初始化遊戲變量
    game_over = False
    game_close = False
    
    # 初始化蛇的初始位置和速度等變數
    x1 = dis_width / 2
    y1 = dis_height / 2
 
    x1_change = 0
    y1_change = 0
 
    snake_List = []
    Length_of_snake = 1
    
    # 隨機生成食物的位置
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
    
    # 開始主要遊戲迴圈，直到遊戲結束
    while not game_over:
        
        # 如果遊戲結束，則顯示結束訊息，並等待玩家選擇重新開始或結束遊戲
        while game_close == True:
            dis.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            Your_score(Length_of_snake - 1)
            pygame.display.update()
 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        # 處理所有的事件，包括玩家按鍵操作和關閉窗口等
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
        # 如果蛇撞到邊界，則設置遊戲結束的標誌
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        # 移動蛇的頭部
        x1 += x1_change
        y1 += y1_change

        # 重新繪製遊戲畫面
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        
        # 更新蛇的位置和長度
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # 檢查蛇是否與自身碰
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        # 畫出蛇及更新分數
        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)

        # 更新畫面
        pygame.display.update()

        # 如果蛇吃到食物，產生新的食物，並增加蛇的長度
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        # 控制遊戲的速度
        clock.tick(snake_speed)
 
    pygame.quit()
    quit()
 
 
gameLoop()