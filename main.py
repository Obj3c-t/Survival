import pygame, sys, random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

pygame.display.set_caption("2D SURVIVAL - PHASE 1")

clock = pygame.time.Clock()

class Resource:
	def __init__(self, x, y, resource_type):
		super(Resource, self).__init__()
		self.rect = pygame.Rect(x, y, 32, 32)
		self.type = resource_type
		self.health = 100

		if self.type == "tree":
			self.color = (34, 139, 34)
		elif self.type == "rock":
			self.color = (128, 128, 128)

	def draw(self, surface):
		pygame.draw.rect(surface, self.color, self.rect)

player_rect = pygame.Rect(400, 300, 32, 32)
player_speed = 4


resources_list = []
GRID_SIZE = 32

for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
	for x in range(0, SCREEN_WIDTH, GRID_SIZE):
		if abs(x - 400) < 64 and abs(y - 300) < 64:
			continue

		spawn_chance = random.randint(1, 100)

		if spawn_chance <= 5: # 5% chance to spawn
			resources_list.append(Resource(x, y, "tree"))
		elif spawn_chance <=8: # 3% chance to spawn
			resources_list.append(Resource(x, y, "rock"))

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	keys = pygame.key.get_pressed()

	if keys[pygame.K_LEFT] or keys[pygame.K_a]:
		player_rect.x -= player_speed
	if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
		player_rect.x += player_speed
	if keys[pygame.K_UP] or keys[pygame.K_w]:
		player_rect.y -= player_speed
	if keys[pygame.K_DOWN] or keys[pygame.K_s]:
		player_rect.y += player_speed
	
	screen.fill((101,146,90))

	for resource in resources_list:
		resource.draw(screen)

	pygame.draw.rect(screen, (255,255,255), player_rect)

	pygame.display.flip()
	clock.tick(60)
