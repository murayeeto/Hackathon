import pygame 
from game_data import levels
from support import import_folder
from decoration import Sky

class Node(pygame.sprite.Sprite):
	def __init__(self,pos,status,icon_speed,path,layer,node_text=''):
		super().__init__()
		self.frames = import_folder(path)
		self.frame_index = 0
		self.image = self.frames[self.frame_index]
		if status == 'available':
			self.status = 'available'
		else:
			self.status = 'locked'

		self.rect = self.image.get_rect(center = pos)
		self.node_text = node_text
		self.layer = layer
		self.font = pygame.font.Font(None, 45)  # Set the font for the text
		self.text_surface = self.font.render(self.node_text, True, (255, 255, 255))  # Render the text surface
		self.text_rect = self.text_surface.get_rect(center=self.rect.center)
		self.text_displayed = False	

		self.detection_zone = pygame.Rect(self.rect.centerx-(icon_speed/2),self.rect.centery-(icon_speed/2),icon_speed,icon_speed)

	def animate(self):
		self.frame_index += 0.15
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]


	def update(self):
		if self.status == 'available':
			self.animate()
		else:
			tint_surf = self.image.copy()
			tint_surf.fill('black',None,pygame.BLEND_RGBA_MULT)
			self.image.blit(tint_surf,(0,0))

		self.fixed_text_position = (600, 550)

	def draw_text(self, surface, is_selected):
		if self.status == 'available' and is_selected:
			fixed_text_rect = self.text_surface.get_rect(center=self.fixed_text_position)
			surface.blit(self.text_surface, fixed_text_rect)

class Icon(pygame.sprite.Sprite):
	def __init__(self,pos):
		super().__init__()
		self.pos = pos
		self.image = pygame.image.load('../graphics/overworld/hat.png').convert_alpha()
		self.rect = self.image.get_rect(center = pos)

	def update(self):
		self.rect.center = self.pos

class Overworld:
	def __init__(self,start_level,max_level,surface,create_level):

		# setup 
		self.display_surface = surface 
		self.max_level = max_level
		self.current_level = start_level
		self.create_level = create_level
		self.selected_node = None

		# movement logic
		self.moving = False
		self.move_direction = pygame.math.Vector2(0,0)
		self.speed = 8

		# sprites 
		self.setup_nodes()
		self.setup_icon()
		self.sky = Sky(8,'../graphics/decoration/sky/space.png')

		# time 
		self.start_time = pygame.time.get_ticks()
		self.allow_input = False
		self.timer_length = 300

	def setup_nodes(self):
		self.nodes = pygame.sprite.LayeredUpdates()
		for index, node_data in enumerate(levels.values()):
			layer = index
			node_text = node_data.get('node_text', '')
			node_sprite = Node(node_data['node_pos'], 'available', self.speed, node_data['node_graphics'], layer, node_text)
			self.nodes.add(node_sprite)

	def draw_paths(self):
		if self.max_level > 0:
			points = [node['node_pos'] for index,node in enumerate(levels.values()) if index <= self.max_level]
			pygame.draw.lines(self.display_surface,'#a04f45',False,points,7)

	def setup_icon(self):
		self.icon = pygame.sprite.GroupSingle()
		icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
		self.icon.add(icon_sprite)

	def input(self):
		keys = pygame.key.get_pressed()

		if not self.moving and self.allow_input:
			if keys[pygame.K_RIGHT] and self.current_level < self.max_level-1:
				self.move_direction = self.get_movement_data('next')
				self.current_level += 1
				self.selected_node = self.nodes.sprites()[self.current_level]
				self.moving = True
			elif keys[pygame.K_LEFT] and self.current_level > 0:
				self.move_direction = self.get_movement_data('previous')
				self.current_level -= 1
				self.selected_node = self.nodes.sprites()[self.current_level]
				self.moving = True
			elif keys[pygame.K_SPACE]:
				self.create_level(self.current_level)


	def get_movement_data(self,target):
		start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
		
		if target == 'next': 
			end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)
		else:
			end = pygame.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)

		return (end - start).normalize()

	def update_icon_pos(self):
		if self.moving and self.move_direction:
			self.icon.sprite.pos += self.move_direction * self.speed
			target_node = self.nodes.sprites()[self.current_level]
			if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
				self.moving = False
				self.move_direction = pygame.math.Vector2(0,0)

	def input_timer(self):
		if not self.allow_input:
			current_time = pygame.time.get_ticks()
			if current_time - self.start_time >= self.timer_length:
				self.allow_input = True

	def run(self):
		# Draw text for each node

		self.sky.draw(self.display_surface)

		self.draw_paths()
		self.input_timer()
		self.input()
		self.update_icon_pos()
		self.icon.update()
		self.nodes.update()

		for node in self.nodes:
			node.draw_text(self.display_surface, node == self.selected_node)
		
		# Draw nodes after text
		self.nodes.draw(self.display_surface)
		
		self.icon.draw(self.display_surface)

		pygame.display.flip()

