import pygame
from tiles import AnimatedTile, StaticTile
from support import import_folder
from random import choice, randint
from settings import vertical_tile_number, tile_size, screen_width

class Sky:
    def __init__(self, intensity, image_path, style='level'):
        self.intensity = intensity
        self.image = pygame.image.load(image_path).convert_alpha()
        self.style = style
        # Stretch
        self.image = pygame.transform.scale(self.image, (screen_width, vertical_tile_number * tile_size))
 
    def draw(self, surface):
        surface.blit(self.image, (0, 0))

        if self.style == 'overworld':
            if self.style == 'overworld':
                self.palms = []
                self.clouds = [] 



class Clouds:
    def __init__(self, horizon, level_width, cloud_number):
        if cloud_number > 0:
            cloud_surf_list = import_folder('../graphics/decoration/clouds')
            min_x = -screen_width
            max_x = level_width + screen_width
            min_y = 0
            max_y = horizon
            self.cloud_sprites = pygame.sprite.Group()

            for cloud in range(cloud_number):
                cloud = choice(cloud_surf_list)
                x = randint(min_x, max_x)
                y = randint(min_y, max_y)
                sprite = StaticTile(0, x, y, cloud)
                self.cloud_sprites.add(sprite)
        else:
            self.cloud_sprites = pygame.sprite.Group()

    def draw(self, surface, shift):
        self.cloud_sprites.update(shift)
        self.cloud_sprites.draw(surface)

class Water:
    def __init__(self, top, level_width):
        water_start = -screen_width
        water_tile_width = 192
        tile_x_amount = int((level_width + screen_width * 2) / water_tile_width)
        self.water_sprites = pygame.sprite.Group()

        for tile in range(tile_x_amount):
            x = tile * water_tile_width + water_start
            y = top
            sprite = AnimatedTile(192, x, y, '../graphics/decoration/water')
            self.water_sprites.add(sprite)

    def draw(self, surface, shift):
        self.water_sprites.update(shift)
        self.water_sprites.draw(surface)

class Clouds:
	def __init__(self,horizon,level_width,cloud_number):
		cloud_surf_list = import_folder('../graphics/decoration/clouds')
		min_x = -screen_width
		max_x = level_width + screen_width
		min_y = 0
		max_y = horizon
		self.cloud_sprites = pygame.sprite.Group()

		for cloud in range(cloud_number):
			cloud = choice(cloud_surf_list)
			x = randint(min_x,max_x)
			y = randint(min_y,max_y)
			sprite = StaticTile(0,x,y,cloud)
			self.cloud_sprites.add(sprite)

	def draw(self,surface,shift):
		self.cloud_sprites.update(shift)
		self.cloud_sprites.draw(surface)
