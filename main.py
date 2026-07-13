# Note for Stardance Reviewers:
# I am using Gemini to help me understand and to learn to make different processes
# such as the complex math parts for scrolling camera or the inventory and is all documented in the commits
# All main logic and design are done by me
# in my hackatime, i originally had a platformer folder that i reused to make this
# however i quickly ditched that platformer and it shows as a different project even though i started coding this and renamed it later

# GAME CONFIG & BASIC SETTINGS
import pygame, sys, random, math

pygame.init()

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 1000

TILE_SCALE = 2
BASE_TILE_SIZE = 32

TILE_SIZE = BASE_TILE_SIZE * TILE_SCALE

WORLD_WIDTH = SCREEN_WIDTH * 12
WORLD_HEIGHT = SCREEN_HEIGHT * 12

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
structure_blueprints = {0: [], 1: []}
active_resources = []

active_structures = []
player_level = 1
player_xp = 0
player_xp_needed = 100

XP_REWARDS = {
	"tree": 20,
	"rock": 35,
	"copper_ore": 50,
	"iron_ore": 75,
	"cow": 30,
	"enemy": 60
}

respawn_queue = []

RESOURCE_SPAWN_CONFIG =  {
	0: {
		"tree": {"respawn_time": 1200,"spawn_chance": 0.85,  "max_per_biome": 40},
		"rock": {"respawn_time": 1800,"spawn_chance": 0.70,	"max_per_biome": 25},
		"copper_ore": {"respawn_time": 2400,"spawn_chance": 0.45,"max_per_biome": 15},
		"iron_ore": {"respawn_time": 3000,"spawn_chance": 0.35,"max_per_biome": 10},
		"solarite_ore": {"respawn_time": 4500,"spawn_chance": 0.15, "max_per_biome": 4}
	},

	1: {
		"tree": {"respawn_time": 3600, "spawn_chance": 0.15, "max_per_biome": 3},
	    "rock": {"respawn_time": 1800, "spawn_chance": 0.30, "max_per_biome": 10},
	    "copper_ore": {"respawn_time": 2400, "spawn_chance": 0.55, "max_per_biome": 20},
	    "iron_ore": {"respawn_time": 3000, "spawn_chance": 0.45, "max_per_biome": 15},
	    "solarite_ore": {"respawn_time": 4500, "spawn_chance": 0.20, "max_per_biome": 5}
	}
	
}

ITEM_REGISTRY = {
	"Wood": {"color": (139, 69, 19), "is_structure":False, "structure_type": None },
	"Stone": {"color": (128, 128, 128), "is_structure": False, "structure_type": None},
	"Copper Ore": {"color": (184, 115, 51), "is_structure": False, "structure_type": None},
	"Iron Ore": {"color": (165, 42, 42), "is_structure": False, "structure_type": None},
	"Solarite Ore": {"color": (255, 140, 0), "is_structure": False, "structure_type": None},
	"Copper Bar": {"color": (212, 115, 71), "is_structure": False, "structure_type": None},
	"Iron Bar": {"color": (210, 210, 210), "is_structure": False, "structure_type": None},
	"Solarite Bar": {"color": (255, 69, 0), "is_structure": False, "structure_type": None},
	"Leather": {"color": (150, 90, 50), "is_structure": False, "structure_type": None},
	"Leather Armor": {"color": (100, 65, 35), "is_structure": False, "structure_type": None},
	"Fists": {
		"color": (240,240,240), "is_structure": False, "structure_type": None,
		"swing_duration": 10, "arc_range": math.pi / 2, "blade_length":35, "trail_color": (200,220,255,150)
	},
	"Wooden Sword": {
		"color": (170, 110, 50), "is_structure": False, "structure_type": None,
		"swing_duration": 14, "arc_range": math.pi * 0.7, "blade_length": 55, "trail_color": (210, 180, 140, 180)
	},
	"Stone Sword": {
		"color": (150, 150, 150), "is_structure": False, "structure_type": None,
		"swing_duration": 18, "arc_range": math.pi * 0.8, "blade_length": 65, "trail_color": (180, 180, 180, 200)
	},
	"Stone Pickaxe": {
		"color": (190, 190, 190), "is_structure": False, "structure_type": None,
		"swing_duration": 22, "arc_range": math.pi * 0.5, "blade_length": 50, "trail_color": (130, 200, 240, 160)
	},
	"Copper Sword": {
		"color": (195, 105, 60), "is_structure": False, "structure_type": None,
		"swing_duration": 16, "arc_range": math.pi * 0.8, "blade_length": 75, "trail_color": (230, 150, 100, 200)
	},
	"Iron Sword": {
		"color": (220, 220, 225), "is_structure": False, "structure_type": None,
		"swing_duration": 15, "arc_range": math.pi * 0.85, "blade_length": 75, "trail_color": (240, 240, 255, 220)
	},
	"Solarite Sword": {
		"color": (255, 90, 0), "is_structure": False, "structure_type": None,
		"swing_duration": 12, "arc_range": math.pi * 0.95, "blade_length": 85, "trail_color": (255, 180, 100, 240)
	},
	"Workbench": {"color": (160, 110, 60), "is_structure": True, "structure_type": "workbench"},
	"Coal Kiln": {"color": (40,40,45), "is_structure": True, "structure_type": "coal_kiln"},
	"Furnace": {"color": (80, 80, 80), "is_structure": True, "structure_type": "furnace"},
	"Anvil": {"color": (50, 50, 55), "is_structure": True, "structure_type": "anvil"},
	"Coal": {"color": (20,20,20), "is_structure": False, "structure_type": None}
}

RECIPES = [
	{"result": "Workbench", "ingredients": {"Wood": 10}, "station": None},
	{"result": "Coal Kiln", "ingredients": {"Stone": 20, "Wood": 10}, "station": "workbench"},
	{"result": "Furnace", "ingredients": {"Stone": 25, "Wood": 5}, "station": "coal_kiln"},
	{"result": "Anvil", "ingredients": {"Iron Bar": 5}, "station": "workbench"},
	{"result": "Stone Pickaxe", "ingredients": {"Wood": 4, "Stone": 8}, "station": "workbench"},
	{"result": "Leather Armor", "ingredients": {"Leather": 15}, "station": "workbench"},
	{"result": "Wooden Sword", "ingredients": {"Wood": 6}, "station": None},
	{"result": "Stone Sword", "ingredients": {"Wood": 4, "Stone": 8}, "station": "workbench"},
	{"result": "Coal", "ingredients": {"Wood": 2}, "station": "coal_kiln", "duration": 180},
	{"result": "Copper Bar", "ingredients": {"Copper Ore": 3, "Coal": 1}, "station": "furnace", "duration": 240},
	{"result": "Iron Bar", "ingredients": {"Iron Ore": 3, "Coal": 1}, "station": "furnace", "duration": 300},
	{"result": "Solarite Bar", "ingredients": {"Solarite Ore": 3, "Coal": 2}, "station": "furnace", "duration": 420},
	{"result": "Copper Sword", "ingredients": {"Wood": 2, "Copper Bar": 5}, "station": "anvil"},
	{"result": "Iron Sword", "ingredients": {"Wood": 2, "Iron Bar": 5}, "station": "anvil"},
	{"result": "Solarite Sword", "ingredients": {"Wood": 2, "Solarite Bar": 6}, "station": "anvil"}
]

# player_inventory = {
	# "tree": 0,
	# "rock": 0
# }
# inventory_slots = {
	# 0: {"item": None, "count": 0, "color": None},
	# 1: {"item": None, "count": 0, "color": None},
	# 2: {"item": None, "count": 0, "color": None},
	# 3: {"item": None, "count": 0, "color": None},
	# 4: {"item": None, "count": 0, "color": None},
	# 5: {"item": None, "count": 0, "color": None},
	# 6: {"item": None, "count": 0, "color": None},
	# 7: {"item": None, "count": 0, "color": None},
	# 8: {"item": None, "count": 0, "color": None},
	# 9: {"item": None, "count": 0, "color": None},
	# 10: {"item": None, "count": 0, "color": None},
	# 11: {"item": None, "count": 0, "color": None},
# }
TOTAL_SLOTS = 24
inventory_slots = {i: {"item": None, "count": 0, "color": None} for i in range(TOTAL_SLOTS)}
armor_slot = {"item": None, "count": 0, "color": None}

is_inventory_open = False
selected_hotbar_slot = 0
terminal_input_buffer = ""
is_console_open = False
console_input_text = ""
dragged_item = None
drag_source_slot = None

# GAME OBJECTS &  MAIN CLASSES
class PlacedStructure:
	def __init__(self, world_x, world_y, struct_type, color):
		self.rect = pygame.Rect(world_x, world_y, TILE_SIZE, TILE_SIZE)
		self.type = struct_type
		self.color = color
		self.active_production = None
	def update(self):
		if self.active_production is not None:
			self.active_production["timer"] += 1
			if self.active_production["timer"] >= self.active_production["max_duration"]:
				res_item = self.active_production["result"]
				res_meta = ITEM_REGISTRY[res_item]
				add_item_to_inventory(res_item, res_meta["color"], 1)
				self.active_production = None

	def draw(self, surface, camera_x, camera_y):
		screen_x = self.rect.x - camera_x
		screen_y = self.rect.y - camera_y
		if -TILE_SIZE <= screen_x <= SCREEN_WIDTH and -TILE_SIZE <= screen_y <= SCREEN_HEIGHT:
			pygame.draw.rect(surface, self.color,(screen_x,screen_y,TILE_SIZE, TILE_SIZE), border_radius=4)
			pygame.draw.rect(surface, (255,255,255), (screen_x,screen_y,TILE_SIZE,TILE_SIZE), 2, border_radius=4)
			lbl_surf = ui_font.render(self.type.upper(), True, (255, 255, 255))
			surface.blit(lbl_surf, (screen_x + (TILE_SIZE // 2) - (lbl_surf.get_width() // 2), screen_y - 18))

			if self.active_production is not None:
				bar_w = TILE_SIZE
				bar_h = 6
				bx = screen_x
				by = screen_y - 6
				pygame.draw.rect(surface, (30,30,30), (bx, by, bar_w, bar_h), border_radius=2)
				pct = self.active_production["timer"] / self.active_production["max_duration"]
				pygame.draw.rect(surface, (255, 165, 0), (bx, by, int(bar_w * pct), bar_h), border_radius= 2)

class Resource:
	def __init__(self, world_x, world_y, resource_type):
		super(Resource, self).__init__()
		self.rect = pygame.Rect(world_x, world_y, TILE_SIZE, TILE_SIZE)
		self.type = resource_type
		self.max_health = 300
		

		if self.type == "tree":
			self.color = (34, 139, 34)
			self.item_yield = "Wood"
			self.max_health = 200
		elif self.type == "rock":
			self.color = (128, 128, 128)
			self.item_yield = "Stone"
			self.max_health = 300
		elif self.type == "copper_ore":
			self.color = (184, 115, 51)
			self.item_yield = "Copper Ore"
			self.max_health = 500
		elif self.type == "iron_ore":
			self.color = (165, 42, 42)
			self.item_yield = "Iron Ore"
			self.max_health = 900
		elif self.type == "solarite_ore":
			self.color = (255, 140, 0)
			self.item_yield = "Solarite Ore"
			self.max_health = 1700
		self.health = self.max_health


	def draw(self, surface, camera_x, camera_y):
		screen_x = self.rect.x - camera_x
		screen_y = self.rect.y - camera_y
		if -TILE_SIZE <= screen_x <= SCREEN_WIDTH and -TILE_SIZE <= screen_y <= SCREEN_HEIGHT:
			draw_rect = pygame.Rect(screen_x, screen_y, TILE_SIZE, TILE_SIZE)
			pygame.draw.rect(surface, self.color, draw_rect)
active_mobs = []
class CowNPC:
	def __init__(self, world_x, world_y):
		self.rect = pygame.Rect(world_x, world_y, TILE_SIZE, TILE_SIZE)
		self.color = (139, 115, 85)
		self.health = 100
		self.max_health = 100
		self.move_timer = 0
		self.dx = 0
		self.dy = 0
		self.base_speed = 1 * TILE_SCALE
		self.panic_speed = 3.5 * TILE_SCALE
		self.damage_timer = 0
		self.panic_timer = 0

	def update(self):
		if self.damage_timer > 0:
			self.damage_timer -=1
		if self.panic_timer > 0:
			self.panic_timer -=1
			current_speed = self.panic_speed
		else:
			current_speed = self.base_speed


		self.move_timer += 1
		if self.move_timer >= 120:
			self.move_timer = 0
			if random.randint(1, 100) <= 60:
				self.dx = random.choice([-1, 0, 1]) * current_speed
				self.dy = random.choice([-1, 0, 1]) * current_speed
			else:
				self.dx, self.dy = 0,0
		# self.rect.x += self.dx
		# self.rect.y += self.dy

		if self.dx != 0:
			self.rect.x += self.dx
			for obj in active_resources + active_structures:
				if self.rect.colliderect(obj.rect):
					if self.dx > 0:
						self.rect.right = obj.rect.left
					if self.dx < 0:
						self.rect.left = obj.rect.right
		if self.dy != 0:
			self.rect.y += self.dy
			for obj in active_resources + active_structures:
				if self.rect.colliderect(obj.rect):
					if self.dy > 0:
						self.rect.bottom = obj.rect.top
					if self.dy < 0:
						self.rect.top = obj.rect.bottom

		if self.rect.x < 0: self.rect.x = 0
		if self.rect.x > WORLD_WIDTH - TILE_SIZE: self.rect.x = WORLD_WIDTH - TILE_SIZE
		if self.rect.y < 0: self.rect.y = 0
		if self.rect.y > WORLD_HEIGHT - TILE_SIZE: self.rect.y = WORLD_HEIGHT - TILE_SIZE

	def start_panic(self, player_x, player_y):
		self.panic_timer = 150
		cow_center_x = self.rect.centerx
		cow_center_y = self.rect.centery
		away_angle = math.atan2(cow_center_y - player_y, cow_center_x - player_x)

		angle_offset = random.uniform(-0.2, 0.2)
		self.dx = math.cos(away_angle + angle_offset) * self.panic_speed
		self.dy = math.sin(away_angle + angle_offset) * self.panic_speed

	def draw(self, surface, camera_x, camera_y):
		screen_x = self.rect.x - camera_x
		screen_y = self.rect.y - camera_y
		if -TILE_SIZE <= screen_x <= SCREEN_WIDTH and -TILE_SIZE <= screen_y <= SCREEN_HEIGHT:
			if self.damage_timer > 0:
				shake_offset = math.sin(self.damage_timer * 5) * 8
				screen_x += shake_offset
			mob_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
			pygame.draw.rect(mob_surf, self.color, (0, 0, TILE_SIZE, TILE_SIZE), border_radius = 6)
			pygame.draw.rect(mob_surf, (60,45,30), (8,8, 12, 12), border_radius=2)

			if self.damage_timer > 0:
				red_mask = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
				red_mask.fill((255, 0, 0, 140))
				mob_surf.blit(red_mask, (0,0), special_flags=pygame.BLEND_RGBA_ADD)
			surface.blit(mob_surf, (screen_x, screen_y))
			if self.health < self.max_health:
				bar_w = TILE_SIZE
				pygame.draw.rect(surface, (50,50,50), (screen_x, screen_y - 10, bar_w, 6))
				pct = max(0.0, self.health / self.max_health)
				pygame.draw.rect(surface, (255, 50, 50), (screen_x, screen_y - 10, int(bar_w * pct), 6))

# PLAYER INIT
player_width = 24 * TILE_SCALE
player_height = 24 * TILE_SCALE
player_world_x = WORLD_WIDTH // 2
player_world_y = WORLD_HEIGHT // 2
player_speed = 3 * TILE_SCALE
harvest_range = TILE_SIZE * 2
active_harvest_target = None
harvest_progress = 0
# WORLD GEN ENGINES
player_max_health = 100
player_current_health = 100
player_damage_timer = 0
desert_damage_timer = 0

is_swinging = False
swing_timer = 0
swing_duration = 12
swing_angle = 0

entity_respawn_timer = 0
MAX_COWS_IN_FOREST = 6

def generate_all_biomes_at_start(): 
	world_blueprints.clear()
	for biome_idx in range(len(biomes)):
		world_blueprints[biome_idx] = []
		for y in range(0, WORLD_HEIGHT, TILE_SIZE):
			for x in range(0, WORLD_WIDTH, TILE_SIZE):
				if abs(x - WORLD_WIDTH // 2) < TILE_SIZE * 3 and abs(y - WORLD_HEIGHT // 2) < TILE_SIZE * 3:
					continue
				tile_occupied = False
				# spawn_roll = random.randint(0, 100)
				if biome_idx == 0:
					if random.randint(0, 100) <= 10: # 4% chance to spawn
						world_blueprints[biome_idx].append({"x": x, "y": y, "type": "tree"})
						tile_occupied = True

					if not tile_occupied and random.randint(0, 100) <= 3: # 2% chance to spawn
						world_blueprints[biome_idx].append({"x": x, "y": y, "type": "rock"})
						tile_occupied = True

				elif biome_idx == 1:
					if random.randint(0, 100) <= 1: # Trees are exceptionally rare
						world_blueprints[biome_idx].append({"x": x, "y": y, "type": "tree"})
						tile_occupied = True
					if not tile_occupied and random.randint(0, 100) <= 3: # 3% Copper chance
						world_blueprints[biome_idx].append({"x": x, "y": y, "type": "copper_ore"})
						tile_occupied = True
					if not tile_occupied and random.randint(0, 100) <= 3: # 2% Iron chance
						world_blueprints[biome_idx].append({"x": x, "y": y, "type": "iron_ore"})
						tile_occupied = True
					if not tile_occupied and random.randint(0, 100) <= 1:
						world_blueprints[biome_idx].append({"x": x, "y":y, "type": "solarite_ore"})
						tile_occupied = True
def load_current_biome_objects():
	active_resources.clear()
	active_structures.clear()
	active_mobs.clear()
	blueprint_list = world_blueprints[current_biome_index]
	for data in blueprint_list:
		active_resources.append(Resource(data["x"], data["y"], data["type"]))

	for s_data in structure_blueprints[current_biome_index]:
		active_structures.append(PlacedStructure(s_data["x"], s_data["y"], s_data["type"], s_data["color"]))

	if current_biome_index == 0:
		for _ in range(5):
			cx = random.randint(100, WORLD_WIDTH - 100)
			cy = random.randint(100,WORLD_HEIGHT - 100)
			active_mobs.append(CowNPC(cx,cy))
# core world setup
generate_all_biomes_at_start()
load_current_biome_objects()

ui_font = pygame.font.SysFont("SFProRoundedRegular", 14, bold=True)
hud_font = pygame.font.SysFont("SFProRoundedRegular", 18, bold=True)
def add_item_to_inventory(item_name, item_color, amount=1):
	for slot_idx in range(TOTAL_SLOTS):
		if inventory_slots[slot_idx]["item"] == item_name:
			inventory_slots[slot_idx]["count"] += amount
			return
	for slot_idx in range(TOTAL_SLOTS):
		if inventory_slots[slot_idx]["item"] is None:
			inventory_slots[slot_idx]["item"] = item_name
			inventory_slots[slot_idx]["count"] = amount
			inventory_slots[slot_idx]["color"] = item_color
			return

def get_total_inventory_counts():
	counts = {}
	for data in inventory_slots.values():
		if data["item"] is not None:
			counts[data["item"]] = counts.get(data["item"], 0) + data["count"] 
	if armor_slot["item"] is not None:
		counts[armor_slot["item"]] = counts.get(armor_slot["item"], 0) + armor_slot["count"]
	return counts

def deduct_crafting_resources(ingredients):
	for item, req_amt in ingredients.items():
		rem = req_amt
		for idx in range(TOTAL_SLOTS):
			if inventory_slots[idx]["item"] == item:
				if inventory_slots[idx]["count"] >= rem:
					inventory_slots[idx]["count"] -= rem
					rem = 0
				else:
					rem -= inventory_slots[idx]["count"]
					inventory_slots[idx]["count"] = 0
				if inventory_slots[idx]["count"] == 0:
					inventory_slots[idx] = {"item": None, "count": 0, "color": None}
			if rem == 0:
				break

def scan_nearby_crafting_stations():
	stations = set()
	player_center_x = player_world_x + (player_width // 2)
	player_center_y = player_world_y + (player_height // 2)
	for struct in active_structures:
		dist = math.hypot(player_center_x - struct.rect.centerx, player_center_y - struct.rect.centery)
		if dist <= harvest_range:
			stations.add(struct.type)
	return stations

def process_xp_gain(amount):
	global player_xp, player_level, player_xp_needed
	player_xp += amount
	while player_xp>= player_xp_needed:
		player_xp -= player_xp_needed
		player_level += 1
		player_xp_needed = player_level * 100



def draw_hud_and_inventories(surface):
	mouse_pos = pygame.mouse.get_pos()
	slot_size = 50
	padding = 10

	hovered_item_name = None

	xp_bar_w, xp_bar_h = 400,12
	xp_x = (SCREEN_WIDTH //2) - (xp_bar_w // 2)
	xp_y = 20
	pygame.draw.rect(surface, (30,30,30), (xp_x, xp_y,xp_bar_w,xp_bar_h), border_radius=6)
	xp_pct = min(1.0, player_xp / player_xp_needed)
	pygame.draw.rect(surface, (0,180,255), (xp_x + 2, xp_y+2, int((xp_bar_w-4) * xp_pct), xp_bar_h-4), border_radius=4)

	hp_bar_w, hp_bar_h = 200, 16
	hp_x = 20
	hp_y = 20
	pygame.draw.rect(surface, (30,30,30), (hp_x, hp_y, hp_bar_w, hp_bar_h), border_radius=4)
	hp_pct = max(0.0, min(1.0, player_current_health / player_max_health))
	pygame.draw.rect(surface, (240, 50, 50), (hp_x + 2, hp_y + 2, int((hp_bar_w - 4) * hp_pct), hp_bar_h - 4), border_radius=2)
	hp_txt = ui_font.render(f"HP: {player_current_health}/{player_max_health}", True, (255,255,255))
	surface.blit(hp_txt, (hp_x + 5, hp_y + 1))

	p_cx = player_world_x + (player_width // 2)
	p_cy = player_world_y + (player_height // 2)
	wb_count = 0
	for struct in active_structures:
		if struct.type == "workbench":
			wb_count += 1
			wb_cx = struct.rect.centerx
			wb_cy = struct.rect.centery
			dist = int(math.hypot(wb_cx - p_cx, wb_cy - p_cy) // TILE_SIZE)
			s_wb_x = wb_cx - camera_x
			s_wb_y = wb_cy - camera_y

			if s_wb_x < 20 or s_wb_x > SCREEN_WIDTH - 20 or s_wb_y < 20 or s_wb_y > SCREEN_HEIGHT - 20:
				angle = math.atan2(wb_cy - p_cy, wb_cx - p_cx)
				edge_x = max(40, min(SCREEN_WIDTH - 40, int(SCREEN_WIDTH // 2 + math.cos(angle) * (SCREEN_WIDTH // 2 - 50))))
				edge_y = max(60, min(SCREEN_HEIGHT - 60, int(SCREEN_HEIGHT // 2 + math.sin(angle) * (SCREEN_HEIGHT // 2 - 80))))
				pygame.draw.circle(surface, (30,30,30), (edge_x, edge_y), 18)
				pygame.draw.circle(surface, (160, 110, 60), (edge_x, edge_y), 18, 2)
				track_lbl = ui_font.render(f"BASE {wb_count} ({dist}m)", True, (255, 235, 180))
				surface.blit(track_lbl, (edge_x - track_lbl.get_width() // 2, edge_y + 20 if edge_y < SCREEN_HEIGHT - 100 else edge_y - 32))

	if active_harvest_target is not None and pygame.mouse.get_pressed()[0]:
		bar_w, bar_h = 200, 20
		bar_x = (SCREEN_WIDTH // 2) - (bar_w // 2)
		bar_y = SCREEN_HEIGHT - 130

		pygame.draw.rect(surface, (30,30,30), (bar_x, bar_y, bar_w, bar_h), border_radius = 4)

		pct = harvest_progress / active_harvest_target.max_health
		pygame.draw.rect(surface, (0,220,100), (bar_x + 2, bar_y + 2, int((bar_w - 4) * pct), bar_h - 4), border_radius=2)

		txt = hud_font.render("Harvesting...", True, (255,255,255))
		surface.blit(txt, (SCREEN_WIDTH //2 - txt.get_width() // 2, bar_y - 25))
	hotbar_w = (slot_size * 4) + (padding * 5)
	hotbar_h = slot_size + (padding * 2)
	hotbar_x = (SCREEN_WIDTH // 2) - (hotbar_w // 2)
	hotbar_y = SCREEN_HEIGHT - hotbar_h - 15

	pygame.draw.rect(surface, (45, 45, 45, 220), (hotbar_x, hotbar_y, hotbar_w, hotbar_h), border_radius=8)
	pygame.draw.rect(surface, (120, 120, 120) if selected_hotbar_slot is not None else (80,80,80), (hotbar_x, hotbar_y, hotbar_w, hotbar_h), 2, border_radius=8)
	hotbar_rects = {}
	for idx in range(4):
		sx = hotbar_x + padding + (idx * (slot_size + padding))
		sy = hotbar_y + padding
		slot_rect = pygame.Rect(sx,sy,slot_size,slot_size)
		hotbar_rects[idx] = slot_rect
		bg_color = (60,60,60) if idx == selected_hotbar_slot else (25,25,25)
		pygame.draw.rect(surface, bg_color, slot_rect, border_radius=5)
		pygame.draw.rect(surface, (200,200,200) if idx == selected_hotbar_slot else (80,80,80), slot_rect,2 if idx == selected_hotbar_slot else 1, border_radius=5)

		slot_data = inventory_slots[idx]
		if slot_data["item"] is not None and drag_source_slot != idx:
			pygame.draw.rect(surface, slot_data["color"], (sx + 8, sy + 8, slot_size - 16, slot_size - 16), border_radius=3)
			cnt_txt = ui_font.render(str(slot_data["count"]), True, (255,255,255))
			surface.blit(cnt_txt, (sx + slot_size - cnt_txt.get_width() - 5, sy + slot_size - cnt_txt.get_height() - 3))

		if slot_rect.collidepoint(mouse_pos):
			hovered_item_name = slot_data["item"]
	inv_grid_rects = {}
	craft_panel_rects = []
	armor_slot_rect = pygame.Rect(0,0,0,0)
	trash_slot_rect = pygame.Rect(0,0,0,0)

	if is_inventory_open:
		inv_w = (slot_size * 5) + (padding * 6) + 120
		inv_h = (slot_size * 4) + (padding * 5) + 60
		inv_x = (SCREEN_WIDTH // 2) - (inv_w // 2) - 130
		inv_y = (SCREEN_HEIGHT // 2) - (inv_h // 2) - 30

		pygame.draw.rect(surface, (35, 35, 35), (inv_x, inv_y, inv_w, inv_h), border_radius=10)
		pygame.draw.rect(surface, (150, 150, 150), (inv_x, inv_y, inv_w, inv_h), 2, border_radius=10)

		title = hud_font.render("Inventory (E to Close)", True, (240,240,240))
		surface.blit(title, (inv_x + padding + 5, inv_y + 12))

		slot_start_idx = 4
		for row in range(4):
			for col in range(5):
				idx = slot_start_idx + (row * 5) + col
				sx = inv_x + padding + (col * (slot_size + padding))
				sy = inv_y + 40 + padding + (row * (slot_size + padding))
				slot_rect = pygame.Rect(sx, sy, slot_size, slot_size)
				inv_grid_rects[idx] = slot_rect

				pygame.draw.rect(surface, (20, 20, 20), slot_rect, border_radius=5)
				pygame.draw.rect(surface, (70, 70, 70), slot_rect, 1, border_radius=5)

				slot_data = inventory_slots[idx]
				if slot_data["item"] is not None and drag_source_slot != idx:
					pygame.draw.rect(surface, slot_data["color"], (sx + 8, sy + 8, slot_size - 16, slot_size - 16), border_radius=3)
					cnt_txt = ui_font.render(str(slot_data["count"]), True, (255,255,255))
					surface.blit(cnt_txt, (sx + slot_size - cnt_txt.get_width() - 5, sy + slot_size - cnt_txt.get_height() - 3))
				if slot_rect.collidepoint(mouse_pos):
					hovered_item_name = slot_data["item"]
		asx = inv_x + (5 * (slot_size + padding)) + padding + 20
		asy = inv_y + 60
		armor_slot_rect = pygame.Rect(asx, asy, slot_size, slot_size)
		pygame.draw.rect(surface, (25, 35, 45), armor_slot_rect, border_radius=5)
		pygame.draw.rect(surface, (0,150, 255), armor_slot_rect, 1 if drag_source_slot == "armor" else 2, border_radius = 5)
		as_lbl = ui_font.render("ARMOR", True, (0, 150, 255))
		surface.blit(as_lbl, (asx + (slot_size//2) - as_lbl.get_width()//2, asy - 18))
		if armor_slot["item"] is not None and drag_source_slot != "armor":
			pygame.draw.rect(surface, armor_slot["color"], (asx + 8, asy + 8, slot_size - 16, slot_size - 16), border_radius=3)
			acnt = ui_font.render(str(armor_slot["count"]), True, (255,255,255))
			surface.blit(acnt, (asx + slot_size - acnt.get_width() - 5, asy + slot_size - acnt.get_height() - 3))
		if armor_slot_rect.collidepoint(mouse_pos):
			hovered_item_name = armor_slot["item"]

		tsx = asx
		tsy = asy + slot_size + 40
		trash_slot_rect = pygame.Rect(tsx, tsy, slot_size, slot_size)
		pygame.draw.rect(surface, (45, 20, 20), trash_slot_rect, border_radius=5)
		pygame.draw.rect(surface, (255, 50, 50), trash_slot_rect, 2, border_radius=5)

		ts_lbl = ui_font.render("TRASH", True, (255, 50, 50))
		surface.blit(ts_lbl, (tsx + (slot_size//2) - ts_lbl.get_width()//2, tsy - 18))
		if trash_slot_rect.collidepoint(mouse_pos):
			hovered_item_name = "Trash Bin (Click with item to remove)"

		craft_x = inv_x + inv_w + 20
		craft_w = 280
		craft_h = 45 + (len(RECIPES) * 38) + 15
		pygame.draw.rect(surface, (30,30,30,240), (craft_x, inv_y, craft_w, craft_h), border_radius = 10)
		pygame.draw.rect(surface, (100,100,100), (craft_x, inv_y, craft_w, craft_h), 2, border_radius=10)
		c_title = hud_font.render("Crafting", True, (0, 200, 255))
		surface.blit(c_title, (craft_x + 15, inv_y + 12))

		current_inv_counts = get_total_inventory_counts()
		active_stations = scan_nearby_crafting_stations()

		entry_y = inv_y + 45
		for recipe in RECIPES:
			station_match = recipe["station"] is None or recipe["station"] in active_stations
			has_mats = all(current_inv_counts.get(item, 0) >= amt for item, amt in recipe["ingredients"].items())

			if station_match:
				item_lbl = f"{recipe['result']}"
				text_color = (255,255,255) if has_mats else (100,100,100)

				row_rect = pygame.Rect(craft_x + 10, entry_y, craft_w - 20, 32)
				craft_panel_rects.append({"rect": row_rect, "recipe": recipe, "valid": has_mats})

				bg_row = (45,45,45) if has_mats else (20,20,20)
				pygame.draw.rect(surface, bg_row, row_rect, border_radius=4)

				meta = ITEM_REGISTRY[recipe["result"]]
				pygame.draw.rect(surface, meta["color"], (craft_x + 15, entry_y+8, 16, 16), border_radius = 2)

				lbl_surface = ui_font.render(item_lbl, True, text_color)
				surface.blit(lbl_surface, (craft_x + 40, entry_y + 8))

				req_strings = [f"{amt} {it[:3]}" for it, amt in recipe["ingredients"].items()]
				req_surface = ui_font.render(", ".join(req_strings), True, (160,160,160) if has_mats else (140,70,70))
				surface.blit(req_surface, (craft_x + craft_w - req_surface.get_width() - 15, entry_y + 8))

				entry_y += 38

	if dragged_item is not None:
		ds = 36
		mx, my = mouse_pos
		pygame.draw.rect(surface, dragged_item["color"], (mx - ds//2, my - ds//2, ds, ds), border_radius=3)
		c_txt = ui_font.render(str(dragged_item["count"]), True, (255,255,255))
		surface.blit(c_txt, (mx + ds//2 - c_txt.get_width(), my + ds//2 - c_txt.get_height()))
	

	if hovered_item_name is not None and dragged_item is None:
		tip_txt = ui_font.render(hovered_item_name, True, (255,255,255))
		tip_w = tip_txt.get_width() + 12
		tip_h = tip_txt.get_height() + 8
		tx = mouse_pos[0] + 12
		ty = mouse_pos[1] + 12
		if tx + tip_w > SCREEN_WIDTH: tx = SCREEN_WIDTH - tip_w - 5
		if ty + tip_h > SCREEN_HEIGHT: ty = SCREEN_HEIGHT - tip_h - 5

		pygame.draw.rect(surface, (20, 20 ,20, 240), (tx, ty, tip_w, tip_h), border_radius=4)
		pygame.draw.rect(surface, (100, 100, 100), (tx, ty, tip_w, tip_h), 1, border_radius=4)
		surface.blit(tip_txt, (tx + 6, ty + 4))
	return hotbar_rects, inv_grid_rects, craft_panel_rects, armor_slot_rect, trash_slot_rect



# def draw_graphical_inventory(surface):
# 	bar_width = 240
# 	bar_height = 70
# 	bar_x = (SCREEN_WIDTH // 2) - (bar_width // 2)
# 	bar_y = SCREEN_HEIGHT - bar_height - 20

# 	hud_panel = pygame.Surface((bar_width, bar_height), pygame.SRCALPHA)
# 	hud_panel.fill((40,40,40, 200))
# 	pygame.draw.rect(hud_panel, (200,200,200), (0,0,bar_width, bar_height), 2, border_radius = 8)
# 	surface.blit(hud_panel, (bar_x, bar_y))

# 	slots = [
# 		{"type": "tree", "color": (34, 139, 34), "label": "Wood"},
# 		{"type": "tree", "color": (128, 128, 128), "label": "Stone"}
# 	]

# 	slot_size = 46
# 	start_offset_x = bar_x + 20
# 	slot_y = bar_y + 12

# 	for i, slot in enumerate(slots):
# 		current_x = start_offset_x + (i * (slot_size + 30))

# 		# draw item container frame
# 		pygame.draw.rect(surface, (20,20,20), (current_x, slot_y, slot_size, slot_size), border_radius=4)
# 		pygame.draw.rect(surface, (100,100,100), (current_x, slot_y, slot_size, slot_size), border_radius=4)

# 		# render mini colored icon
# 		pygame.draw.rect(surface, slot["color"], (current_x + 8, slot_y + 8, slot_size - 16, slot_size - 16))

# 		# render stack text counters
# 		count_val = player_inventory[slot["type"]]
# 		text_surface = ui_font.render(str(count_val), True, (255,255,255))
# 		surface.blit(text_surface, (current_x + slot_size - text_surface.get_width() - 4, slot_y + slot_size - text_surface.get_height() - 2))

# 		#render title labels
# 		label_surface = ui_font.render(slot["label"], True, (230,230,230))
# 		surface.blit(label_surface, (current_x + (slot_size//2) - (label_surface.get_width() // 2), slot_y - 18))
def process_console_cheat_command(command_text):
	global player_current_health, player_max_health
	
	parts = command_text.strip().split()
	if not parts:
		return

	base_cmd = parts[0].lower()

	if base_cmd == "heal":
		player_current_health = player_max_health
		print("[CONSOLE CHEAT] Health fully restored!")

	elif base_cmd == "give" and len(parts) >= 2:
		if parts[-1].isdigit():
			amount = int(parts[-1])
			item_name = " ".join(parts[1:-1])
		else:
			amount = 1
			item_name = " ".join(parts[1:])

		# Convert input names to title case if they match registry keys
		# E.g., 'wood' -> 'Wood', 'solarite ore' -> 'Solarite Ore'
		matched_key = None
		for key in ITEM_REGISTRY.keys():
			if key.lower() == item_name.lower():
				matched_key = key
				break

		if matched_key:
			meta = ITEM_REGISTRY[matched_key]
			add_item_to_inventory(matched_key, meta["color"], amount)
			print(f"[CONSOLE CHEAT] Added {amount}x {matched_key} to inventory.")
		else:
			print(f"[CONSOLE CHEAT] Error: '{item_name}' not found in ITEM_REGISTRY.")
			
	elif base_cmd == "xp" and len(parts) >= 2:
		if parts[1].isdigit():
			amt = int(parts[1])
			process_xp_gain(amt)
			print(f"[CONSOLE CHEAT] Awarded {amt} XP.")
	else:
		print("[CONSOLE CHEAT] Unknown command. Try: 'heal', 'xp 500', or 'give wood 50'")

def process_resource_respawns():
	global active_resources, world_blueprints

	for item in list(respawn_queue):
		item["timer"] -= 1

		if item["timer"] <= 0:
			res_type = item["type"]
			target_biome = item["biome_index"]
			config = RESOURCE_SPAWN_CONFIG[target_biome][res_type]

			current_count = sum(1 for bp in world_blueprints[target_biome] if bp["type"] == res_type)
			if current_count < config["max_per_biome"]:
				if random.random() <= config["spawn_chance"]:
					valid_spot = False
					attempts = 0

					while not valid_spot and attempts < 30:
						attempts += 1
						rx = (random.randint(50, WORLD_WIDTH - 100) // TILE_SIZE) * TILE_SIZE
						ry = (random.randint(50, WORLD_HEIGHT - 100) // TILE_SIZE) * TILE_SIZE

						if abs(rx - WORLD_WIDTH // 2) < TILE_SIZE * 3 and abs(ry - WORLD_HEIGHT // 2) < TILE_SIZE * 3:
							continue

						test_rect = pygame.Rect(rx, ry, TILE_SIZE, TILE_SIZE)
						player_rect = pygame.Rect(player_world_x, player_world_y, player_width, player_height)

						overlap = any(test_rect.colliderect(s.rect) for s in active_structures)
						if target_biome == current_biome_index:
							overlap = overlap or any(test_rect.colliderect(r.rect) for r in active_resources)
						else:
							overlap = overlap or any(bp["x"] == rx and bp["y"] == ry for bp in world_blueprints[target_biome])
						if not overlap and not test_rect.colliderect(player_rect):
							valid_spot = True
							world_blueprints[target_biome].append({"x": rx, "y": ry, "type": res_type})
							if target_biome == current_biome_index:
								active_resources.append(Resource(rx, ry, res_type))
			respawn_queue.remove(item)
# MAIN ENGINE LOOP
while True:
	mouse_x, mouse_y = pygame.mouse.get_pos()
	for struct in active_structures:
		struct.update()

	hotbar_rects, inv_grid_rects, craft_panel_rects, armor_slot_rect, trash_slot_rect = draw_hud_and_inventories(screen)

	# EVENT PROCESSING
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN:

			if is_console_open:
				if event.key == pygame.K_BACKQUOTE or event.key == pygame.K_ESCAPE:
					is_console_open = False
				elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
					print(f"[Executing]: {console_input_text}")
					process_console_cheat_command(console_input_text)
					console_input_text = ""
					is_console_open = False  # Close console after entering cheat
				elif event.key == pygame.K_BACKSPACE:
					console_input_text = console_input_text[:-1]
				else:
					# Append the actual text character typed
					if event.unicode:
						console_input_text += event.unicode
			else:			
				if event.key == pygame.K_e:
					is_inventory_open = not is_inventory_open
					if not is_inventory_open and dragged_item is not None:
						inventory_slots[drag_source_slot] = dragged_item
						dragged_item = None
						drag_source_slot = None
				elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
					selected_hotbar_slot = event.key - pygame.K_1
				elif event.key == pygame.K_BACKQUOTE: # The ` key right next to the 1 key
					is_console_open = True
					print("\n>>> CHEAT SYSTEM LISTENING: Click your terminal window and type your command, then press Enter! <<<")
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				clicked_slot = None
				is_armor_click = False

				for idx, r in hotbar_rects.items():
					if r.collidepoint(mouse_x, mouse_y):
						clicked_slot = idx
						selected_hotbar_slot = idx
						break

				if is_inventory_open:
					for idx, r in inv_grid_rects.items():
						if r.collidepoint(mouse_x, mouse_y):
							clicked_slot = idx
							break

					if trash_slot_rect.collidepoint(mouse_x, mouse_y):
						if dragged_item is not None:
							dragged_item = None
							drag_source_slot = None

					if armor_slot_rect.collidepoint(mouse_x, mouse_y):
						is_armor_click = True

					for entry in craft_panel_rects:
						if entry["rect"].collidepoint(mouse_x,mouse_y) and entry["valid"]:

							rcp = entry["recipe"]
							if "duration" in rcp:
								target_station = None	
								p_cx = player_world_x + (player_width // 2)
								p_cy = player_world_y + (player_height // 2)

								for struct in active_structures:
									if struct.type == rcp["station"] and struct.active_production is None:
										dist = math.hypot(p_cx - struct.rect.centerx, p_cy - struct.rect.centery)
										if dist <= harvest_range:
											target_station = struct
											break
								if target_station is not None:
									deduct_crafting_resources(rcp["ingredients"])
									target_station.active_production = {
										"result": rcp["result"],
										"timer": 0,
										"max_duration": rcp["duration"]
									}
								else:
									print("[SYSTEM] no available processin station nearby!")
							else:
								deduct_crafting_resources(rcp["ingredients"])
								res_meta = ITEM_REGISTRY[rcp["result"]]
								add_item_to_inventory(rcp["result"], res_meta["color"], 1)
							break

				if is_armor_click:
					if dragged_item is None:
						if armor_slot["item"] is not None:
							dragged_item = armor_slot.copy()
							drag_source_slot = "armor"
							armor_slot = {"item": None, "count": 0, "color": None}
					else:
						if "Armor" in dragged_item["item"]:
							target_slot_data = armor_slot.copy()
							armor_slot = dragged_item

							if target_slot_data["item"] is not None:
								dragged_item = target_slot_data
								drag_source_slot = "armor"
							else:
								dragged_item = None
								drag_source_slot = None

				elif clicked_slot is not None:
					if dragged_item is None:
						if inventory_slots[clicked_slot]["item"] is not None:
							dragged_item = inventory_slots[clicked_slot].copy()
							drag_source_slot = clicked_slot
							inventory_slots[clicked_slot] = {"item": None, "count": 0, "color": None}
					else:
						target_slot_data = inventory_slots[clicked_slot].copy()
						inventory_slots[clicked_slot] = dragged_item

						if target_slot_data["item"] is not None:
							dragged_item = target_slot_data
							drag_source_slot = clicked_slot
						else:
							dragged_item = None
							drag_source_slot = None

	mouse_pressed = pygame.mouse.get_pressed()
	if mouse_pressed[0] and not is_inventory_open and dragged_item is None:
		click_world_x = mouse_x + camera_x
		click_world_y = mouse_y + camera_y

		player_center_x = player_world_x + (player_width // 2)
		player_center_y = player_world_y + (player_height //2)

		active_hand_item = inventory_slots[selected_hotbar_slot]["item"]

		if not is_swinging:
			is_swinging = True
			swing_timer = 0
			swing_angle = math.atan2(click_world_y - player_center_y, click_world_x - player_center_x)

			weapon_meta = ITEM_REGISTRY.get(active_hand_item, ITEM_REGISTRY["Fists"])
			if "swing_duration" in weapon_meta:
				swing_duration = weapon_meta["swing_duration"]
			else:
				swing_duration = 12

		if active_hand_item and ITEM_REGISTRY[active_hand_item]["is_structure"]:
			snap_x = (click_world_x // TILE_SIZE) * TILE_SIZE
			snap_y = (click_world_y // TILE_SIZE) * TILE_SIZE

			build_dist = math.hypot(player_center_x - (snap_x + TILE_SIZE//2), player_center_y - (snap_y + TILE_SIZE//2))
			if build_dist <= harvest_range:
				space_occupied = False
				test_rect = pygame.Rect(snap_x, snap_y, TILE_SIZE, TILE_SIZE)

				for r in active_resources:
					if test_rect.colliderect(r.rect): space_occupied = True
				for s in active_structures:
					if test_rect.colliderect(s.rect): space_occupied = True
				if test_rect.colliderect(pygame.Rect(player_world_x, player_world_y, player_width,player_height)):
					space_occupied = True

				if not space_occupied:
					meta = ITEM_REGISTRY[active_hand_item]
					active_structures.append(PlacedStructure(snap_x, snap_y, meta["structure_type"], meta["color"]))
					structure_blueprints[current_biome_index].append({
						"x": snap_x,
						"y": snap_y,
						"type": meta["structure_type"],
						"color": meta["color"]
						})

					inventory_slots[selected_hotbar_slot]["count"] -= 1
					if inventory_slots[selected_hotbar_slot]["count"] <= 0:
						inventory_slots[selected_hotbar_slot] = {"item": None, "count": 0, "color": None}

		reach_x = player_center_x + math.cos(swing_angle) * (TILE_SIZE * 1.2)
		reach_y = player_center_y + math.sin(swing_angle) * (TILE_SIZE * 1.2)
		attack_hitbox = pygame.Rect(reach_x - 20, reach_y - 20,40,40)



		for mob in list(active_mobs):
			if attack_hitbox.colliderect(mob.rect):
				if swing_timer == 1:
					base_attack_damage = 5
					if active_hand_item == "Wooden Sword":
						base_attack_damage = 10
					if active_hand_item == "Stone Sword":
						base_attack_damage = 20
					if active_hand_item == "Stone Pickaxe":
						base_attack_damage = 7
					mob.health -= base_attack_damage
					mob.damage_timer = 20
					# mob.rect.x += math.cos(swing_angle) * 24
					# mob.rect.y += math.sin(swing_angle) * 24
					mob.start_panic(player_world_x, player_world_y)
					if mob.health <= 0:
						add_item_to_inventory("Leather", ITEM_REGISTRY["Leather"]["color"], random.randint(1, 2))
						process_xp_gain(XP_REWARDS["cow"])
						active_mobs.remove(mob)


		hovered_res = None
		for res in active_resources:
			if res.rect.collidepoint(click_world_x, click_world_y):
				dist = math.hypot(player_center_x - res.rect.centerx, player_center_y - res.rect.centery)
				if dist <= harvest_range:
					hovered_res = res
					break
		if hovered_res is not None:
			if active_harvest_target != hovered_res:
				active_harvest_target = hovered_res
				harvest_progress = 0

			active_hand_item = inventory_slots[selected_hotbar_slot]["item"]
			harvest_speed = 1

			if active_hand_item == "Stone Pickaxe":
				if active_harvest_target.type == "rock":
					harvest_speed = 5
				elif active_harvest_target.type in ["copper_ore", "iron_ore"]:
					harvest_speed = 3
				elif active_harvest_target.type == "tree":
					harvest_speed = 2
				elif active_harvest_target.type == "solarite_ore":
					harvest_speed = 2

			harvest_progress += harvest_speed

			if harvest_progress >= active_harvest_target.max_health:
				add_item_to_inventory(active_harvest_target.item_yield, active_harvest_target.color)
				if active_harvest_target.type in XP_REWARDS:
					process_xp_gain(XP_REWARDS[active_harvest_target.type])
				if active_harvest_target.type in RESOURCE_SPAWN_CONFIG[current_biome_index]:
					respawn_queue.append({
							"biome_index": current_biome_index,
							"type": active_harvest_target.type,
							"timer": RESOURCE_SPAWN_CONFIG[current_biome_index][active_harvest_target.type]["respawn_time"]
						})

				blueprint_list = world_blueprints[current_biome_index]
				for bp in blueprint_list:
					if (bp["x"] == active_harvest_target.rect.x and
						 bp["y"] == active_harvest_target.rect.y and
						 bp["type"] == active_harvest_target.type):
						blueprint_list.remove(bp)
						break

				active_resources.remove(active_harvest_target)
				active_harvest_target = None
				harvest_progress = 0
		else:
			active_harvest_target = None
			harvest_progress = 0

	else:
		if not mouse_pressed[0]:
			active_harvest_target = None
			harvest_progress = 0

				# mouse_x, mouse_y = pygame.mouse.get_pos()

				# click_world_x = mouse_x + camera_x
				# click_world_y = mouse_y + camera_y

				# player_center_x = player_world_x + (player_width // 2)
				# player_center_y = player_world_y + (player_height // 2)

				# for i in range(len(active_resources) -1, -1, -1):
				# 	res= active_resources[i]

				# 	if res.rect.collidepoint(click_world_x, click_world_y):
				# 		dist = math.hypot(player_center_x - res.rect.centerx, player_center_y - res.rect.centery)

				# 		if dist <= harvest_range:
				# 			res.health -= 25
				# 			if res.health <= 0:
				# 				player_inventory[res.type] += 1

				# 				blueprint_list = world_blueprints[current_biome_index]
				# 				for bp in blueprint_list:
				# 					if bp["x"] == res.rect.x and bp["y"] == res.rect.y:
				# 						blueprint_list.remove(bp)
				# 			break


	# INPUT
	keys = pygame.key.get_pressed()
	# X AXIS MOVEMENT AND COLLISION
	dx = 0
	if not is_console_open:
		if keys[pygame.K_LEFT] or keys[pygame.K_a]:
			dx -= player_speed
		if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
			dx += player_speed

	player_world_x += dx
	player_rect = pygame.Rect(player_world_x, player_world_y, player_width, player_height)
	for obj in active_resources + active_structures:
		if player_rect.colliderect(obj.rect):
			if dx > 0:
				player_world_x = obj.rect.left - player_width
			if dx < 0:
				player_world_x = obj.rect.right
	# Y AXIS MOVEMENT AND COLLISION
	dy = 0	
	if not is_console_open:
		if keys[pygame.K_UP] or keys[pygame.K_w]:
			dy -= player_speed
		if keys[pygame.K_DOWN] or keys[pygame.K_s]:
			dy += player_speed
	player_world_y += dy
	player_rect = pygame.Rect(player_world_x, player_world_y, player_width, player_height)
	for obj in active_resources + active_structures:
		if player_rect.colliderect(obj.rect):
			if dy > 0:
				player_world_y = obj.rect.top - player_height
			if dy < 0:
				player_world_y = obj.rect.bottom
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

	if player_damage_timer > 0:
		player_damage_timer -= 1

	for mob in active_mobs:
		mob.update()

	if is_swinging:
		swing_timer += 1
		if swing_timer >= swing_duration:
			is_swinging = False
			swing_timer = 0


	if current_biome_index == 0:
		if len(active_mobs) < MAX_COWS_IN_FOREST:
			entity_respawn_timer +=1
			if entity_respawn_timer >= 600:
				entity_respawn_timer = 0
				left_bound_end = player_world_x - 400
				right_bound_start = player_world_x + 400

				top_bound_end = player_world_y - 400
				bottom_bound_start = player_world_y + 400

				possible_x = []
				if left_bound_end >= 50:
					possible_x.append(random.randint(50,left_bound_end))
				if right_bound_start <= WORLD_WIDTH - 50:
					possible_x.append(random.randint(right_bound_start, WORLD_WIDTH - 50))
				rx = random.choice(possible_x) if possible_x else random.randint(50, WORLD_WIDTH - 50)

				possible_y = []
				if top_bound_end >= 50:
					possible_y.append(random.randint(50, top_bound_end))
				if bottom_bound_start <= WORLD_HEIGHT - 50:
					possible_y.append(random.randint(bottom_bound_start, WORLD_HEIGHT - 50))
				ry = random.choice(possible_y) if possible_y else random.randint(50, WORLD_HEIGHT - 50)

				active_mobs.append(CowNPC(rx, ry))

	else:
		entity_respawn_timer = 0

	if current_biome_index == 1:
		has_protection = armor_slot["item"] == "Leather Armor"
		if not has_protection:
			desert_damage_timer += 1
			if desert_damage_timer >= 60:
				player_current_health -= 5
				player_damage_timer = 20
				desert_damage_timer = 0
				if player_current_health <= 0:
					player_world_x = WORLD_WIDTH // 2
					player_world_y = WORLD_HEIGHT // 2
					current_biome_index = 0
					load_current_biome_objects()
					player_current_health = player_max_health
	else:
		desert_damage_timer = 0
		if player_current_health < player_max_health:
			player_current_health += 0.05

	# CAMERA OFFSET CALCULATIONS
	camera_x = player_world_x - (SCREEN_WIDTH // 2) + (player_width // 2)
	camera_y = player_world_y - (SCREEN_HEIGHT // 2) + (player_height // 2)

	if camera_x < 0: camera_x = 0
	if camera_y < 0: camera_y = 0
	if camera_x > WORLD_WIDTH - SCREEN_WIDTH: camera_x = WORLD_WIDTH - SCREEN_WIDTH
	if camera_y > WORLD_HEIGHT - SCREEN_HEIGHT: camera_y = WORLD_HEIGHT - SCREEN_HEIGHT

	# RENDER GRAPHICS
	screen.fill(biomes[current_biome_index]["grass"])
	for structure in active_structures:
		structure.draw(screen,camera_x, camera_y)

	for resource in active_resources:
		resource.draw(screen, camera_x, camera_y)

	for mob in active_mobs:
		mob.draw(screen, camera_x, camera_y)

	process_resource_respawns()
	player_screen_x = player_world_x - camera_x
	player_screen_y = player_world_y - camera_y

	if player_damage_timer > 0:
		shake_offset = math.sin(player_damage_timer * 1.5) * 8
		player_screen_x +=shake_offset
	player_surf = pygame.Surface((player_width, player_height), pygame.SRCALPHA)
	# player_draw_rect = pygame.Rect(player_screen_x, player_screen_y, player_width, player_height)
	pygame.draw.rect(player_surf, (240,240,240), (0,0, player_width, player_height))

	if player_damage_timer > 0:
		red_mask = pygame.Surface((player_width, player_height), pygame.SRCALPHA)
		red_mask.fill((255, 0, 0, 140))
		player_surf.blit(red_mask, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
	screen.blit(player_surf, (player_screen_x, player_screen_y))

	if is_swinging:
			active_hand_item = inventory_slots[selected_hotbar_slot]["item"]
			
			w_data = ITEM_REGISTRY.get(active_hand_item)
			if w_data is None or "blade_length" not in w_data:
				w_data = ITEM_REGISTRY["Fists"]

			anim_pct = swing_timer / swing_duration
			
			
			duration = w_data["swing_duration"]
			arc_range = w_data["arc_range"]
			length = w_data["blade_length"]
			t_color = w_data["trail_color"]

			p_center_x = player_screen_x + (player_width // 2)
			p_center_y = player_screen_y + (player_height // 2)

			
			trail_points = [(p_center_x, p_center_y)]
			
			
			steps = min(5, swing_timer + 1)
			for i in range(steps):
				
				past_pct = (swing_timer - i) / swing_duration
				past_angle = swing_angle - (arc_range / 2) + (arc_range * past_pct)
				
				tx = p_center_x + math.cos(past_angle) * length
				ty = p_center_y + math.sin(past_angle) * length
				trail_points.append((tx, ty))

			
			if len(trail_points) >= 3:
				trail_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
				
				
				pygame.draw.polygon(trail_surf, t_color, trail_points)
				
				
				lead_angle = swing_angle - (arc_range / 2) + (arc_range * anim_pct)
				lx = p_center_x + math.cos(lead_angle) * length
				ly = p_center_y + math.sin(lead_angle) * length
				pygame.draw.line(trail_surf, (255, 255, 255, 240), (p_center_x, p_center_y), (lx, ly), 3)
				pygame.draw.circle(trail_surf, (255, 255, 255, 255), (int(lx), int(ly)), 3)
				
				
				screen.blit(trail_surf, (0, 0))

	if is_console_open:
		# Translucent black overlay bar across the top
		console_surf = pygame.Surface((SCREEN_WIDTH, 40), pygame.SRCALPHA)
		console_surf.fill((0, 0, 0, 200))
		screen.blit(console_surf, (0, 0))
		
		# Draw text line
		cheat_display_string = f"CHEAT CONSOLE: {console_input_text}_"
		console_render = hud_font.render(cheat_display_string, True, (0, 255, 150))
		screen.blit(console_render, (20, 10))
	draw_hud_and_inventories(screen)
	pygame.display.flip()
	clock.tick(60)

 