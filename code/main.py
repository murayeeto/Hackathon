import pygame, sys
from settings import * 
from level import Level
from overworld import Overworld
from ui import UI

class Game:
	def __init__(self):

		# game attributes
		self.max_level = 8
		self.max_health = 100
		self.cur_health = 100
		self.coins = 0
		
		# audio 
		self.level_bg_music = pygame.mixer.Sound('../audio/level_music.wav')
		self.overworld_bg_music = pygame.mixer.Sound('../audio/overworld_music.wav')

		# overworld creation
		self.overworld = Overworld(0,self.max_level,screen,self.create_level)
		self.status = 'overworld'
		self.overworld_bg_music.play(loops = -1)

		# user interface 
		self.ui = UI(screen)


	def create_level(self,current_level):
		self.level = Level(current_level,screen,self.create_overworld,self.change_coins,self.change_health)
		self.status = 'level'
		self.overworld_bg_music.stop()
		self.level_bg_music.play(loops = -1)

	def create_overworld(self,current_level,new_max_level):
		if new_max_level > self.max_level:
			self.max_level = new_max_level
		self.overworld = Overworld(current_level,self.max_level,screen,self.create_level)
		self.status = 'overworld'
		self.overworld_bg_music.play(loops = -1)
		self.level_bg_music.stop()

	def change_coins(self,amount):
		self.coins += amount

	def change_health(self,amount):
		self.cur_health += amount

	def check_game_over(self):
		if self.cur_health <= 0:
			self.cur_health = 100
			self.coins = 0
			self.max_level = 0
			self.overworld = Overworld(0,self.max_level,screen,self.create_level)
			self.status = 'overworld'
			self.level_bg_music.stop()
			self.overworld_bg_music.play(loops = -1)

	def run_title_screen(self):

		title_screen_image = pygame.image.load('../title.png') 
		title_screen_rect = title_screen_image.get_rect(center=(screen_width // 2, screen_height // 2))


		animation_frames = [pygame.image.load(f'../titleanim/{i}.png') for i in range(1, 23)] 


		for frame in animation_frames:
			screen.blit(frame, title_screen_rect)
			pygame.display.flip()
			pygame.time.delay(30) 


		screen.blit(title_screen_image, title_screen_rect)


		press_space_font = pygame.font.Font(None, 50)
		title_text = press_space_font.render("Space Squad", True, (255, 0, 0))
		press_space_text = press_space_font.render("Press SPACE to Start", True, (255, 0, 0))
		press_space_rect = press_space_text.get_rect(center=(screen_width // 2, screen_height * 2 // 3))
		title_rect = press_space_text.get_rect(center=(screen_width / 1.75, screen_height / 3.5))

		screen.blit(press_space_text, press_space_rect)
		screen.blit(title_text, title_rect)

		pygame.display.flip()


		waiting_for_key = True
		while waiting_for_key:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						waiting_for_key = False


		pygame.time.delay(1000)

		# Transition to the overworld
		self.status = 'overworld'
		self.overworld_bg_music.play(loops=-1)

	def run(self):
				if self.status == 'title':
					self.run_title_screen()
					self.status = 'overworld'
					self.overworld_bg_music.play(loops=-1)

				elif self.status == 'overworld':
					self.overworld.run()

				else:
					self.level.run()
					self.ui.show_health(self.cur_health, self.max_health)
					self.ui.show_coins(self.coins)
					self.check_game_over()


# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
game = Game()
game.run_title_screen()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	
	screen.fill('grey')
	game.run()

	pygame.display.update()
	clock.tick(60)