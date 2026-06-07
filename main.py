# Note for Stardance Reviewers:
# I am using Gemini to help me understand and to learn to make different processes
#such as the complex math for scrolling camera or the inventory
# All main logic and design are done by me
# in my hackatime, i originally had a platformer folder that i reused to make this
# however i quickly ditched that platformer and it shows as a different project even though i started coding this and renamed it later

# GAME CONFIG & BASIC SETTINGS
import pygame, sys, random, math

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

# BIOMES
biomes = [
	{"name": "Forest", "grass": (101, 146, 90)},
	{"name": "Desert", "grass": (225, 191, 117)}
]
current_biome_index = 0
world_blueprints = {}
active_resources = []

player_inventory = {
	"tree": 0,
	"rock": 0
}
# GAME OBJECTS &  MAIN CLASSES
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

# PLAYER INIT
player_width = 24 * TILE_SCALE
player_height = 24 * TILE_SCALE
player_world_x = WORLD_WIDTH // 2
player_world_y = WORLD_HEIGHT // 2
player_speed = 3 * TILE_SCALE

harvest_range = TILE_SIZE * 2.5

# WORLD GEN ENGINES

def generate_all_biomes_at_start():
	world_blueprints.clear()
	for biome_idx in range(len(biomes)):
		world_blueprints[biome_idx] = []
		for y in range(0, WORLD_HEIGHT, TILE_SIZE):
			for x in range(0, WORLD_WIDTH, TILE_SIZE):
				if abs(x - WORLD_WIDTH // 2) < TILE_SIZE * 3 and abs(y - WORLD_HEIGHT // 2) < TILE_SIZE * 3:
					continue

				spawn_roll = random.randint(1, 100)

				if spawn_roll <= 4: # 4% chance to spawn
					world_blueprints[biome_idx].append({"x": x, "y": y, "type": "tree"})
				elif spawn_roll <=6: # 2% chance to spawn
					world_blueprints[biome_idx].append({"x": x, "y": y, "type": "rock"})
def load_current_biome_objects():
	active_resources.clear()
	blueprint_list = world_blueprints[current_biome_index]
	for data in blueprint_list:
		active_resources.append(Resource(data["x"], data["y"], data["type"]))
# core world setup
generate_all_biomes_at_start()
load_current_biome_objects()

ui_font = pygame.font.SysFont("SFProRoundedRegular", 16, bold=True)

def draw_graphical_inventory(surface):
	bar_width = 240
	bar_height = 70
	bar_x = (SCREEN_WIDTH // 2) - (bar_width // 2)
	bar_y = SCREEN_HEIGHT - bar_height - 20

	hud_panel = pygame.Surface((bar_width, bar_height), pygame.SRCALPHA)
	hud_panel.fill((40,40,40, 200))
	pygame.draw.rect(hud_panel, (200,200,200), (0,0,bar_width, bar_height), 2, border_radius = 8)
	surface.blit(hud_panel, (bar_x, bar_y))

	slots = [
		{"type": "tree", "color": (34, 139, 34), "label": "Wood"},
		{"type": "tree", "color": (128, 128, 128), "label": "Stone"}
	]

	slot_size = 46
	start_offset_x = bar_x + 20
	slot_y = bar_y + 12

	for i, slot in enumerate(slots):
		current_x = start_offset_x + (i * (slot_size + 30))

		# draw item container frame
		pygame.draw.rect(surface, (20,20,20), (current_x, slot_y, slot_size, slot_size), border_radius=4)
		pygame.draw.rect(surface, (100,100,100), (current_x, slot_y, slot_size, slot_size), border_radius=4)

		# render mini colored icon
		pygame.draw.rect(surface, slot["color"], (current_x + 8, slot_y + 8, slot_size - 16, slot_size - 16))



# MAIN ENGINE LOOP
while True:
	# EVENT PROCESSING
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	# INPUT
	keys = pygame.key.get_pressed()
	# X AXIS MOVEMENT AND COLLISION
	dx = 0
	if keys[pygame.K_LEFT] or keys[pygame.K_a]:
		dx -= player_speed
	if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
		dx += player_speed

	player_world_x += dx
	player_rect = pygame.Rect(player_world_x, player_world_y, player_width, player_height)
	for resource in active_resources:
		if player_rect.colliderect(resource.rect):
			if dx > 0:
				player_world_x = resource.rect.left - player_width
			if dx < 0:
				player_world_x = resource.rect.right
	# Y AXIS MOVEMENT AND COLLISION
	dy = 0	
	if keys[pygame.K_UP] or keys[pygame.K_w]:
		dy -= player_speed
	if keys[pygame.K_DOWN] or keys[pygame.K_s]:
		dy += player_speed
	player_world_y += dy
	player_rect = pygame.Rect(player_world_x, player_world_y, player_width, player_height)
	for resource in active_resources:
		if player_rect.colliderect(resource.rect):
			if dy > 0:
				player_world_y = resource.rect.top - player_height
			if dy < 0:
				player_world_y = resource.rect.bottom
	# Y AXIS WORLD BOUNDARIES
	if player_world_y < 0: player_world_y = 0
	if player_world_y > WORLD_HEIGHT - player_height: player_world_y = WORLD_HEIGHT - player_height
	# X AXIS BIOME TRANSITIONS
	if player_world_x > WORLD_WIDTH - player_width:
		if current_biome_index +1 < len(biomes):
			current_biome_index += 1
			load_current_biome_objects()
			player_world_x = 10
		else:
			player_world_x = WORLD_WIDTH - player_width
	elif player_world_x < 0:
		if current_biome_index > 0:
			current_biome_index -= 1
			load_current_biome_objects()
			player_world_x = WORLD_WIDTH - player_width - 10
		else:
			player_world_x = 0
	# CAMERA OFFSET CALCULATIONS
	camera_x = player_world_x - (SCREEN_WIDTH // 2) + (player_width // 2)
	camera_y = player_world_y - (SCREEN_HEIGHT // 2) + (player_height // 2)

	if camera_x < 0: camera_x = 0
	if camera_y < 0: camera_y = 0
	if camera_x > WORLD_WIDTH - SCREEN_WIDTH: camera_x = WORLD_WIDTH - SCREEN_WIDTH
	if camera_y > WORLD_HEIGHT - SCREEN_HEIGHT: camera_y = WORLD_HEIGHT - SCREEN_HEIGHT

	# RENDER GRAPHICS
	screen.fill(biomes[current_biome_index]["grass"])

	for resource in active_resources:
		resource.draw(screen, camera_x, camera_y)

	player_screen_x = player_world_x - camera_x
	player_screen_y = player_world_y - camera_y

	player_draw_rect = pygame.Rect(player_screen_x, player_screen_y, player_width, player_height)
	pygame.draw.rect(screen, (240,240,240), player_draw_rect)
	draw_graphical_inventory(screen)
	pygame.display.flip()
	clock.tick(60)
