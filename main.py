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

active_structures = []
player_level = 1
player_xp = 0
player_xp_needed = 100

XP_REWARDS = {
	"tree": 20,
	"rock": 35,
	"enemy": 60
}

ITEM_REGISTRY = {
	"Wood": {"color": (139, 69, 19), "is_structure":False, "structure_type": None },
	"Stone": {"color": (128, 128, 128), "is_structure": False, "structure_type": None},
	"Workbench": {"color": (160, 110, 60), "is_structure": True, "structure_type": "workbench"},
	"Furnace": {"color": (80, 80, 80), "is_structure": True, "structure_type": "furnace"},
	"Anvil": {"color": (50, 50, 55), "is_structure": True, "structure_type": "anvil"},
	"Stone Pickaxe": {"color": (190, 190, 190), "is_structure": False, "structure_type": None}
}

RECIPES = [
	{"result": "Workbench", "ingredients": {"Wood": 10}, "station": None},
	{"result": "Furnace", "ingredients": {"Stone": 20, "Wood": 5}, "station": "workbench"},
	{"result": "Anvil", "ingredients": {"Stone": 30}, "station": "workbench"},
	{"result": "Stone Pickaxe", "ingredients": {"Wood": 4, "Stone": 8}, "station": "workbench"}
]

# player_inventory = {
	# "tree": 0,
	# "rock": 0
# }
inventory_slots = {
	0: {"item": None, "count": 0, "color": None},
	1: {"item": None, "count": 0, "color": None},
	2: {"item": None, "count": 0, "color": None},
	3: {"item": None, "count": 0, "color": None},
	4: {"item": None, "count": 0, "color": None},
	5: {"item": None, "count": 0, "color": None},
	6: {"item": None, "count": 0, "color": None},
	7: {"item": None, "count": 0, "color": None},
	8: {"item": None, "count": 0, "color": None},
	9: {"item": None, "count": 0, "color": None},
	10: {"item": None, "count": 0, "color": None},
	11: {"item": None, "count": 0, "color": None},
}
is_inventory_open = False
selected_hotbar_slot = 0

dragged_item = None
drag_source_slot = None

# GAME OBJECTS &  MAIN CLASSES
class PlacedStructure:
	def __init__(self, world_x, world_y, struct_type, color):
		self.rect = pygame.Rect(world_x, world_y, TILE_SIZE, TILE_SIZE)
		self.type = struct_type
		self.color = color
	def draw(self, surface, camera_x, camera_y):
		screen_x = self.rect.x - camera_x
		screen_y = self.rect.y - camera_y
		if -TILE_SIZE <= screen_x <= SCREEN_WIDTH and -TILE_SIZE <= screen_y <= SCREEN_HEIGHT:
			pygame.draw.rect(surface, self.color,(screen_x,screen_y,TILE_SIZE, TILE_SIZE), border_radius=4)
			pygame.draw.rect(surface, (255,255,255), (screen_x,screen_y,TILE_SIZE,TILE_SIZE), 2, border_radius=4)

class Resource:
	def __init__(self, world_x, world_y, resource_type):
		super(Resource, self).__init__()
		self.rect = pygame.Rect(world_x, world_y, TILE_SIZE, TILE_SIZE)
		self.type = resource_type
		self.max_health = 300
		self.health = self.max_health

		if self.type == "tree":
			self.color = (34, 139, 34)
			self.item_yield = "Wood"
		elif self.type == "rock":
			self.color = (128, 128, 128)
			self.item_yield = "Stone"


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
harvest_range = TILE_SIZE * 2
active_harvest_target = None
harvest_progress = 1
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
	active_structures.clear()
	blueprint_list = world_blueprints[current_biome_index]
	for data in blueprint_list:
		active_resources.append(Resource(data["x"], data["y"], data["type"]))
# core world setup
generate_all_biomes_at_start()
load_current_biome_objects()

ui_font = pygame.font.SysFont("SFProRoundedRegular", 14, bold=True)
hud_font = pygame.font.SysFont("SFProRoundedRegular", 18, bold=True)
def add_item_to_inventory(item_name, item_color, amount=1):
	for slot_idx in range(12):
		if inventory_slots[slot_idx]["item"] == item_name:
			inventory_slots[slot_idx]["count"] += 1
			return
	for slot_idx in range(12):
		if inventory_slots[slot_idx]["item"] is None:
			inventory_slots[slot_idx]["item"] = item_name
			inventory_slots[slot_idx]["count"] = 1
			inventory_slots[slot_idx]["color"] = item_color
			return

def get_total_inventory_counts():
	counts = {}
	for data in inventory_slots.values():
		if data["item"] is not None:
			counts[data["item"]] = counts.get(data["item"], 0) + data["count"] 
	return counts

def deduct_crafting_resources(ingredients):
	for item, req_amt in ingredients.items():
		rem = req_amt
		for idx in range(12):
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

	xp_bar_w, xp_bar_h = 400,12
	xp_x = (SCREEN_WIDTH //2) - (xp_bar_w // 2)
	xp_y = 20
	pygame.draw.rect(surface, (30,30,30), (xp_x, xp_y,xp_bar_w,xp_bar_h), border_radius=6)
	xp_pct = min(1.0, player_xp / player_xp_needed)
	pygame.draw.rect(surface, (0,180,255), (xp_x + 2, xp_y+2, int((xp_bar_w-4) * xp_pct), xp_bar_h-4), border_radius=4)

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

	inv_grid_rects = {}
	craft_panel_rects = []

	if is_inventory_open:
		inv_w = (slot_size * 4) + (padding * 5)
		inv_h = (slot_size * 2) + (padding * 3) + 40
		inv_x = (SCREEN_WIDTH // 2) - (inv_w // 2) - 150
		inv_y = (SCREEN_HEIGHT // 2) - (inv_h // 2) - 30

		pygame.draw.rect(surface, (35, 35, 35), (inv_x, inv_y, inv_w, inv_h), border_radius=10)
		pygame.draw.rect(surface, (150, 150, 150), (inv_x, inv_y, inv_w, inv_h), 2, border_radius=10)

		title = hud_font.render("Inventory (E to Close)", True, (240,240,240))
		surface.blit(title, (inv_x + padding + 5, inv_y + 12))

		slot_start_idx = 4
		for row in range(2):
			for col in range(4):
				idx = slot_start_idx + (row * 4) + col
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
		craft_x = inv_x + inv_w + 20
		craft_w = 280
		pygame.draw.rect(surface, (30,30,30,240), (craft_x, inv_y, craft_w, inv_h), border_radius = 10)
		pygame.draw.rect(surface, (100,100,100), (craft_x, inv_y, craft_w, inv_h), 2, border_radius=10)
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
	return hotbar_rects, inv_grid_rects, craft_panel_rects





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


# MAIN ENGINE LOOP
while True:
	mouse_x, mouse_y = pygame.mouse.get_pos()

	hotbar_rects, inv_grid_rects, craft_panel_rects = draw_hud_and_inventories(pygame.Surface((1,1)))

	# EVENT PROCESSING
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_e:
				is_inventory_open = not is_inventory_open
				if not is_inventory_open and dragged_item is not None:
					inventory_slots[drag_source_slot] = dragged_item
					dragged_item = None
					drag_source_slot = None
			elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
				selected_hotbar_slot = event.key - pygame.K_1
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				clicked_slot = None

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

					for entry in craft_panel_rects:
						if entry["rect"].collidepoint(mouse_x,mouse_y) and entry["valid"]:
							rcp = entry["recipe"]
							deduct_crafting_resources(rcp["ingredients"])
							res_meta = ITEM_REGISTRY[rcp["result"]]
							add_item_to_inventory(rcp["result"], res_meta["color"], 1)
							break
				if clicked_slot is not None:
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

					inventory_slots[selected_hotbar_slot]["count"] -= 1
					if inventory_slots[selected_hotbar_slot]["count"] <= 0:
						inventory_slots[selected_hotbar_slot] = {"item": None, "count": 0, "color": None}

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
				elif active_harvest_target.type == "tree":
					harvest_speed = 2

			harvest_progress += harvest_speed

			if harvest_progress >= active_harvest_target.max_health:
				add_item_to_inventory(active_harvest_target.item_yield, active_harvest_target.color)
				if active_harvest_target.type in XP_REWARDS:
					process_xp_gain(XP_REWARDS[active_harvest_target.type])
				blueprint_list = world_blueprints[current_biome_index]
				for bp in blueprint_list:
					if bp["x"] == active_harvest_target.rect.x and bp["y"] == active_harvest_target.rect.y:
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

	player_screen_x = player_world_x - camera_x
	player_screen_y = player_world_y - camera_y

	player_draw_rect = pygame.Rect(player_screen_x, player_screen_y, player_width, player_height)
	pygame.draw.rect(screen, (240,240,240), player_draw_rect)
	draw_hud_and_inventories(screen)
	pygame.display.flip()
	clock.tick(60)
