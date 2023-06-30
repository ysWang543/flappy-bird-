import pygame,random
from pygame.locals import *

# 初始化 Pygame
pygame.init()

# 設定遊戲視窗大小
screen_width = 288
screen_height = 512
screen = pygame.display.set_mode((288,512))


# 設定遊戲標題
pygame.display.set_caption('Flappy Bird 正常版')

# 定義字體
font = pygame.font.SysFont('None', 60)

# 定義顏色
white = (255, 255, 255)

#遊戲速度
clock = pygame.time.Clock()  # 建立時鐘物件，用於控制遊戲的幀率
fps = 60  # 遊戲的幀率設定為60幀每秒

#遊戲變數設定
ground_scroll = 0  # 地面滾動的初始位置
scroll_speed = 2  # 地面滾動的速度

flying = False  # 鳥的飛行狀態，初始為False
game_over = False  # 遊戲結束狀態，初始為False

pipe_gap = 200  # 管道之間的間隔距離
pipe_frequency = 2000  # 生成管道的頻率，單位為毫秒
last_pipe = pygame.time.get_ticks() - pipe_frequency  # 上一次生成管道的時間

score = 0  # 玩家得分
pass_pipe = False  # 是否通過了管


# 載入遊戲圖片
button_img = pygame.image.load('D:\正常版/restart.png')
background = pygame.image.load('D:\正常版/background.png')
ground_img = pygame.image.load('D:\正常版/ground.png')

# 用於在螢幕上輸出文字的函式
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))
	
# 重設遊戲狀態的函式
def reset_game():
	pipe_group.empty() # 清空水管群組
	# 重設 Flappy 角色的位置
	flappy.rect.x = 100
	flappy.rect.y = int(screen_height / 2)
	# 將分數重設為 0
	score = 0
	# 返回最終的分數值
	return score


class Bird(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) # 初始化父类
        self.images = []  # 存放鸟的图片列表
        self.index = 0    # 图片索引
        self.counter = 0  # 计数器
        for num in range(1, 4):  # 载入鸟的图片
            img = pygame.image.load(f"D:\正常版/bird{num}.png")
            self.images.append(img)
        self.image = self.images[self.index]   # 设置初始图片
        self.rect = self.image.get_rect()      # 获取图片的矩形区域
        self.rect.center = [x, y]   # 设置图片的初始位置
        self.vel = 0    # 鸟的垂直速度
        self.clicked = False    # 点击状态

    def update(self):
        if flying == True:
            # 飞行状态下应用重力
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        if game_over == False:
            # 处理跳跃逻辑
            keys = pygame.key.get_pressed()
            if keys[K_SPACE] and self.clicked == False:
                self.clicked = True
                self.vel = -10 # 设置向上跳跃的速度
            if not keys[K_SPACE]:
                self.clicked = False


			


class Pipe(pygame.sprite.Sprite):

	def __init__(self, x, y, position):
		pygame.sprite.Sprite.__init__(self)	# 初始化父類別
		self.image = pygame.image.load("D:\正常版/pipe.png")	 # 載入管道的圖片
		self.rect = self.image.get_rect()	# 獲取圖片的矩形區域
        # position變數確定管道是從上方還是下方出現
        # position為1代表從上方，-1代表從下方
		if position == 1:
			self.image = pygame.transform.flip(self.image, False, True)	# 垂直翻轉圖片
			self.rect.bottomleft = [x, y - int(pipe_gap / 2)]	# 設定位置在左下方
		elif position == -1:
			self.rect.topleft = [x, y + int(pipe_gap / 2)]	# 設定位置在左上方


	def update(self):
		self.rect.x -= scroll_speed	# 向左移動管道
		if self.rect.right < 0:	# 如果管道超出螢幕範圍，刪除該物件
			self.kill()



class Button():
	def __init__(self, x, y, image):
		self.image = image	# 按鈕的圖片
		self.rect = self.image.get_rect()	# 獲取圖片的矩形區域
		self.rect.topleft = (x, y)	# 設定按鈕的左上角位置

	def draw(self):
		action = False

		# 獲取滑鼠位置
		pos = pygame.mouse.get_pos()

		# 檢查滑鼠是否在按鈕上方並進行點擊條件判斷
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1:	 # 1代表左鍵被按下
				action = True

		 # 繪製按鈕
		screen.blit(self.image, (self.rect.x, self.rect.y))

		return action



pipe_group = pygame.sprite.Group()	# 建立管道群組
bird_group = pygame.sprite.Group()	 # 建立鳥群組

flappy = Bird(100, int(screen_height / 2))	# 創建一個鳥物件

bird_group.add(flappy)	# 將鳥物件加入鳥群組

# 創建重新開始按鈕物件
button = Button(90, screen_height // 2 - 100, button_img)


run = True	# 遊戲運行狀態
while run:

	clock.tick(fps)  # 控制遊戲更新頻率

	screen.blit(background, (0,0)) # 繪製背景圖片

	pipe_group.draw(screen) # 繪製管道群組中的所有管道
	bird_group.draw(screen) # 繪製鳥群組中的所有鳥
	bird_group.update() # 更新鳥的狀態

	screen.blit(ground_img, (ground_scroll, 768)) # 繪製地面圖片並進行滾動

	# 檢查得分
	if len(pipe_group) > 0:
		if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
			and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
			and pass_pipe == False:
			pass_pipe = True
		if pass_pipe == True:
			if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
				score += 1
				pass_pipe = False
	draw_text(str(score), font, white, int(135), 20) # 繪製得分文字


	# 檢查碰撞
	if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
		game_over = True
	# 當鳥觸碰到地面時遊戲結束並停止飛行
	if flappy.rect.bottom >= 768:
		game_over = True
		flying = False


	if flying == True and game_over == False:
		 # 生成新的管道
		time_now = pygame.time.get_ticks()
		if time_now - last_pipe > pipe_frequency:
			pipe_height = random.randint(-100, 100)
			btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
			top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
			pipe_group.add(btm_pipe)
			pipe_group.add(top_pipe)
			last_pipe = time_now
			

		pipe_group.update() # 更新管道的狀態

		ground_scroll -= scroll_speed  # 地面滾動
		if abs(ground_scroll) > 35:
			ground_scroll = 0
	

	# 檢查遊戲結束並重新開始
	if game_over == True:
		if button.draw():
			game_over = False
			score = reset_game()


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
			flying = True

	pygame.display.update() # 更新顯示
 
pygame.quit()  # 關閉遊戲視窗，結束遊戲
