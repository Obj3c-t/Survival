import pygame, sys, random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

TILE_SCALE = 2
BASE_TILE_SIZE = 32

TILE_SIZE = BASE_TILE_SIZE * TILE_SCALE

WORLD_WIDTH = SCREEN_WIDTH * 4
WORLD_HEIGHT = SCREEN_HEIGHT * 4

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

pygame.display.set_caption("2D SURVIVAL - PHASE 1")

clock = pygame.time.Clock()

class Resource:
	def __init__(self, world_x, world_y, resource_type):
		super(Resource, self).__init__()
		self.rect = pygame.Rect(world_x, world_y, TILE_SIZE, TILE_SIZE)
		self.type = resource_type
		self.health = 100

		if self.type == "tree":
			self.color = (34, 139, 34)
		elif self.type == "rock":
			self.color = (128, 128, 128)

	def draw(self, surface, camera_x, camera_y):
		screen_x = self.rect.x - camera_x
		screen_y = self.rect.y - camera_y
		if -TILE_SIZE <= screen_x <= SCREEN_WIDTH and -TILE_SIZE <= screen_y <= SCREEN_HEIGHT:
			draw_rect = pygame.Rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE)
			pygame.draw.rect(surface, self.color, draw_rect)

biomes = [
	{"name": "Forest", "grass": (101, 146, 90)},
	{"name": "Desert", "grass": (225, 191, 117)}
]
current_biome_index = 0


# player_rect = pygame.Rect(400, 300, 32, 32)
# player_speed = 4
player_width = 24 * TILE_SCALE
player_height = 24 * TILE_SCALE
player_world_x = WORLD_WIDTH // 2
player_world_y = WORLD_HEIGHT // 2
player_speed = 3 * TILE_SCALE


resources_list = []
# GRID_SIZE = 32

def generate_map():
	resources_list.clear()

	for y in range(0, WORLD_HEIGHT, TILE_SIZE):
		for x in range(0, WORLD_WIDTH, TILE_SIZE):
			if abs(x - WORLD_WIDTH // 2) < TILE_SIZE * 3 and abs(y - WORLD_HEIGHT // 2) < TILE_SIZE * 3:
				continue

			spawn_roll = random.randint(1, 100)

			if spawn_roll <= 4: # 4% chance to spawn
				resources_list.append(Resource(x, y, "tree"))
			elif spawn_roll <=6: # 2% chance to spawn
				resources_list.append(Resource(x, y, "rock"))

generate_map()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	keys = pygame.key.get_pressed()

	if keys[pygame.K_LEFT] or keys[pygame.K_a]:
		player_world_x -= player_speed
	if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
		player_world_x += player_speed
	if keys[pygame.K_UP] or keys[pygame.K_w]:
		player_world_y -= player_speed
	if keys[pygame.K_DOWN] or keys[pygame.K_s]:
		player_world_y += player_speed
	
	# if player_world_x < 0: player_world_x = 0
	if player_world_y < 0: player_world_y = 0
	if player_world_y > WORLD_HEIGHT - player_height: player_world_y = WORLD_HEIGHT - player_height

	if player_world_x > WORLD_WIDTH - player_width:
		if current_biome_index +1 < len(biomes):
			current_biome_index += 1
			generate_map()
			player_world_x = 10
		else:
			player_world_x = WORLD_WIDTH - player_width
	elif player_world_x < 0:
		if current_biome_index > 0:
			current_biome_index -= 1
			generate_map()
			player_world_x = WORLD_WIDTH - player_width - 10
		else:
			player_world_x = 0

	camera_x = player_world_x - (SCREEN_WIDTH // 2) + (player_width // 2)
	camera_y = player_world_y - (SCREEN_HEIGHT // 2) + (player_height // 2)

	if camera_x < 0: camera_x = 0
	if camera_y < 0: camera_y = 0
	if camera_x > WORLD_WIDTH - SCREEN_WIDTH: camera_x = WORLD_WIDTH - SCREEN_WIDTH
	if camera_y > WORLD_HEIGHT - SCREEN_HEIGHT: camera_y = WORLD_HEIGHT - SCREEN_HEIGHT


	screen.fill(biomes[current_biome_index]["grass"])

	for resource in resources_list:
		resource.draw(screen, camera_x, camera_y)

	player_screen_x = player_world_x - camera_x
	player_screen_y = player_world_y - camera_y

	player_draw_rect = pygame.Rect(player_screen_x, player_screen_y, player_width, player_height)
	pygame.draw.rect(screen, (240,240,240), player_draw_rect)

	pygame.display.flip()
	clock.tick(60)
