import pygame
from global_var import *

fhs = pygame.sprite.Group()

class Comp(pygame.sprite.Sprite):
	def __init__(self):
		super(Comp, self).__init__()
		self.image = pygame.Surface((20, 20))
		self.image.set_colorkey((0,0,0))
		self.color = (63, 159, 255)
		pygame.draw.circle(self.image, self.color, (10, 10), 10)
		self.rect = self.image.get_rect()
		self.rect.center = (WIDTH/2, HEIGHT/2)
		self.add(fhs)
