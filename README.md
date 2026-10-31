# FORGEBOUND (Alpha Build v0.1.0)
*A 2D top-down survival sandbox RPG built in Python with Pygame for the STARDANCE program*


## 1. Game Overview
# FORGEBOUND

FORGEBOUND is a 2D survival sandbox game I'm developing in Python using Pygame.

The game focuses on gathering resources, crafting equipment, building a base, and exploring different biomes. I wanted to combine the progression of games like Terraria and Minecraft with combat that requires more timing and precision.

This is currently an alpha build, so some features are still being worked on.

Players explore a 4 biome world, manage harsh environmental hazards (freezing temperatures, desert heat, and jungle toxicity), smelt advanced metal tiers, brew alchemical potions, and challenge multi phase boss encounters.


## 2. Controls & Core Mechanics

### Basic Controls
| Key / Input | Action | Description |
| :--- | :--- | :--- |
| **W, A, S, D** / Arrows | **Movement** | Moves the character in world space. Subject to sliding ice friction in Tundra and a 40% speed reduction in Jungle mud. |
| **Mouse Cursor** | **Aim** | Aims weapon swings, directional shield blocking, and structure placement. |
| **Left Click** | **Primary Action** | Attacks with equipped weapon, mines resources, places building blocks, or drinks potions from the hotbar. |
| **Right Click (Tap)** | **Perfect Parry** | Activates a strict **12 frame parry window**. Completely negates damage, stuns attackers for 1.5–2.5s, and applies heavy knockback. |
| **Right Click (Hold)** | **Shield Block** | Requires **Iron Shield** equipped. Points shield toward cursor to block 100% damage with mutual knockback separation (has a cooldown bar). |
| **1, 2, 3, 4** | **Hotbar Selection** | Selects active hand item in slots 1–4. |
| **E** | **Inventory & Crafting** | Toggles the 24-slot inventory, armor slot, shield slot, trash bin, and dynamic scrollable crafting menu. |
| **Mouse Wheel** | **Crafting Scroll** | Scrolls through the crafting recipe list inside the clipping viewport. |
| **`** (Backquote) | **Cheat Console** | Opens the developer command console across the top of the screen. |

---

## 3. How to Play & Progression Guide

The game progresses through 4 biomes and 7 gear tiers. To reach the endgame, you should probably follow this progression path:

### Stage 1: The Starter Forest (Tier 1: Wood & Stone)
1. **Harvest Wood & Stone:** Punch or chop trees and rocks to gather basic materials.
2. **Build Your Base:** Craft a **Workbench** (10 Wood) from your crafting menu (`E`). Place it down to unlock advanced recipes.
3. **Craft Starter Gear:** Craft a **Stone Pickaxe** and **Stone Sword** to speed up mining and defend yourself.
4. **Survive the Night:** When night falls (the sun dial in the top right reaches night phase), hostile Zombies, Skeletons, and Slimes will spawn. Build a shelter with **Wooden Walls** and a **Wooden Door**. Craft and click a **Bed** at night to sleep safely until morning.

### Stage 2: The Arid Desert (Tier 2–4: Copper, Iron, Solarite)
1. **Travel East:** Walk east past the world boundary to enter the Desert.
2. **Manage Heat:** The desert sun inflicts steady heat damage unless you wear **Leather Armor** (crafted from cow/scorpion leather) or better.
3. **Advanced Smelting:**
   - Craft a **Coal Kiln** (Stone + Wood) to convert Wood into Coal.
   - Craft a **Furnace** (Stone + Wood) to smelt Copper and Iron Ores with Coal into **Bars**.
   - Craft an **Anvil** (5 Iron Bars) at the Workbench to forge metal swords and pickaxes.
4. **Deep-Vein Solarite:** Explore the deep southern areas of the desert to find rare, glowing orange **Solarite Ore**. Smelt Solarite Bars to forge the **Solarite Sword**, which emits a permanent radius of dynamic light and burns enemies on hit.

### Stage 3: The Glacial Tundra (Tier 5–6: Rimefrost Cobalt & Golem Core)
1. **Travel East from the Desert:** Enter the frozen Tundra.
2. **Cold Hazard & Ice Physics:**
   - Low friction causes you to slide across the snow and ice.
   - A blue **Cold Exposure Meter** fills up. Reaching 100% causes rapid freezing damage.
   - Counter the cold by crafting a **Thermal Lantern** (Solarite Bar + Iron Bar + Coal at the Anvil) or by standing near active Furnaces/Kilns.
3. **Rimefrost Cobalt & The Ice Golem:**
   - Mine blue Cobalt Ore veins using a Solarite Pickaxe. Mining cobalt has a chance to awaken the **Ice Golem miniboss**.
   - Defeat the Ice Golem (watch for his snowball charge and roaring blast telegraphs) to obtain a **Golem Core**.
   - Combine the Golem Core, Wood, and Cobalt Bars at an Anvil to craft the **Cobalt Sword**, which shoots ranged icy projectiles on every swing.

### Stage 4: The Humid Jungle & Alchemy (Tier 7: Verdant Steel)
1. **Travel East from the Tundra:** Enter the toxic Jungle.
2. **Environmental Hazards:**
   - **Mud:** Stepping on patchy brown mud pools cut your movement speed by around 40%.
   - **Toxicity Exposure:** Toxic green fog fills your toxicity meter. Reaching 100% inflicts lethal poison and disables natural health regeneration.
   - **Vine Blockades:** Dense vine barricades block your path, you can slice them with your sword to clear routes.
3. **Alchemist Table & Potions:**
   - Craft an **Alchemist Table** (Wood + Slime Gel at the Workbench).
   - Gather wild **Jungle Herbs** and **Jungle Spores** to brew:
     - **Antidote:** Resets Toxicity exposure to 0%.
     - **Healing Potion:** Instantly restores +40 HP.
     - **Adrenaline Elixir:** Grants a +35% speed boost for 15 seconds to counteract mud.
   - *To drink:* Select the potion in your hotbar and left click.
4. **Verdant Steel Gear:**
   - Mine green **Verdant Ore** near mud pools using your Cobalt Pickaxe.
   - Smelt **Verdant Steel Bars** at the furnace to craft **Verdant Armor** (80% protection + complete immunity to Jungle toxicity) and the **Verdant Sword** (restores +2 HP on every hit).

### Stage 5: The Final Alpha Encounter — Kro'Gath, the Primordial Core
Kro'Gath is located near the western clearing of the Jungle (tracked by the pink **BOSS** radar icon on your HUD).

- **Phase 1 (The Siphon Ward):** Kro'Gath is rooted in place and shielded by an impenetrable barrier that absorbs 100% of sword damage while passively regenerating his health. You must navigate mud pools, dodge incoming needle barrages, and use your **Verdant or Cobalt Pickaxe** to mine down the two glowing **Siphon Conduits** powering his shield.
- **Phase 2 (Uprooted Fury):** Once both conduits are mined to 0 HP, his shell shatters. Kro'Gath uproots, flying freely and pursuing you while ignoring mud slowdown. 
  - **Needle Fans:** Fires 5-way spread shots.
  - **Primordial Charge (The Parry Check):** Flashes a red `!` warning and dashes forward at high speed. You must **Perfect Parry** this dash to stun him for 2.5 seconds, creating your opening to counterattack with your sword.
  - **Soft Enrage:** Below 25% health, toxicity passively rises across the arena, putting a strict timer on your DPS.

---

## 4. Stardance Reviewer Testing & Evaluation Guide

To enable quick evaluation of mid game, late gaem, and boss mechanics without grinding through the progression tree, use the built-in **Developer Console**.

### How to Use the Console
1. Press the **`** key (backquote, located directly to the left of the `1` key).
2. Type any of the commands below and press **Enter**.

### Quick-Test Commands Table
| Command | Effect | Reviewer Testing Purpose |
| :--- | :--- | :--- |
| `heal` | Restores player HP to full | Recovers health during difficult boss tests. |
| `give Verdant Sword 1` | Gives Tier 7 Sword | Tests high melee damage and the +2 HP lifsteal mechanic. |
| `give Verdant Pickaxe 1` | Gives Tier 7 Pickaxe | Tests maximum mining speed on ores and Siphon Conduits. |
| `give Verdant Armor 1` | Gives Tier 7 Armor | Tests 80% damage reduction and total immunity to Jungle toxicity. |
| `give Iron Shield 1` | Gives Iron Shield | Tests 360° directional blocking and the 12-frame parry window. |
| `give Healing Potion 5` | Gives 5 Healing Potions | Tests consumable hotbar drinking and instant +40 HP recovery. |
| `give Antidote 5` | Gives 5 Antidotes | Tests instant toxicity meter reset. |
| `give Adrenaline Elixir 5` | Gives 5 Speed Elixirs | Tests the +35% speed boost when running through mud pools. |
| `give Thermal Lantern 1` | Gives Thermal Lantern | Tests cold mitigation in the Glacial Tundra. |
| `spawn krogath` | Spawns Kro'Gath Boss | Instantly spawns Kro'Gath and his two Siphon Conduits right next to the player anywhere in the world. |
| `spawn icegolem` | Spawns Ice Golem | Tests the Tundra miniboss moveset (snowball charges, roar blast, boulder throws). |
| `spawn hornet` | Spawns Giant Hornet | Tests Jungle aerial enemy AI and stinger projectile dodging. |
| `spawn sporetrap` | Spawns Venus Spore-Trap | Tests proximity-triggered plant turret needles. |
| `mobs` (or `count`) | Toggles Mob Monitor | Displays an on-screen live entity tracker on the HUD showing all active NPC counts. |
| `xp 500` | Grants 500 Player XP | Tests player level-up, max HP scaling, and stat increases. |

---

## 5. Recommended 5-Minute Evaluation Routine

For evaluators looking to verify all major systems quickly:

1. **Test Base Mechanics (1 min):** Punch a tree, press `E` to open inventory, craft a Workbench, and place it.
2. **Test Combat & Parrying (1 min):** Press **`**, type `give Iron Shield 1`, type `spawn scorpion`, and practice tapping **Right-Click** right as the scorpion flashes `!` to execute a Perfect Parry.
3. **Test Biome Hazards & Potions (1 min):** Walk east till you get into the Jungle (or Desert/Tundra) to watch the Toxicity/cold bar rise, or if you take damage. Type `give Antidote 1`, select it on slot 1, and Left-Click to drink and cure yourself.
4. **Test the Final Boss Fight (2 min):**
   - Type give Verdant Sword 1, give Verdant Pickaxe 1, give Verdant Armor 1, and spawn krogath.
   - Hit Kro'Gath with your sword to see his Phase 1 Siphon immunity.
   - Switch to your pickaxe to mine down both glowing Siphon Conduits.
   - Fight Phase 2: Dodge his needle fans, time a parry on his ! charge to stun him, and defeat him.

---

## 6. Academic Integrity & AI Transparency Statement
*Statement for Stardance evaluators:*

I built FORGEBOUND using Python and Pygame. The project includes resource gathering, crafting, combat, enemy AI, and several different biomes.

I'm still working on improving the game and fixing bugs as I go.

I used Gemini to help with some of the more complicated math and development problems. The game is my own project, and I've kept the development history in the repository.

## 7. Final Notes
*Parrying system*

This was probably the most painful thing to work on in this project. Tt was extremely hard to get the timings correct for it to work properly, and shields are still kind of just cosmetic.

*Broken Knockback*

Sometimes the enemies knockback clips through solid resources?? Knockback was quite hard to do so I just gave up on it and since there are resources everywhere, it would kind of be cheesing combat a little.

*Overall...*

I had lots of fun building this project throughout the summer, and considering the time that I have right now, I may take another huge break from working on this. Although im happy where it is right now, I feel like 
it could be so much more. That being said, this will be a long term project for me and the first next step, is to transfer this thing to a different game engine. Thank you Star dance for this wonderful program, and I look forward to doing more Hack Club projects!
