# Name: Antonio Hedgpeth
# Date: February 22, 2026
# gamefunctions.py

"""Module for the game functions.

This provides necessary functions for managing the menus,
basic commands, and generation of random monster encounters."""
import random
import json
from wanderingmonster import WanderingMonster

def purchase_item(itemPrice, startingMoney, quantityToPurchase=1):
    """Args:
        itemPrice (int): The cost per item.
        startingMoney (int): Total money available.
        quantityToPurchase (int): Desired amount.

    Returns:
        tuple: (final_quantity, remaining_money)"""

    """Calculate how many items you can afford with start money"""
    affordable_quantity = startingMoney // itemPrice
    """Limits the purchase to the requested amount or what is affordable"""
    final_quantity = min(quantityToPurchase, affordable_quantity)
    """Calculates the remaining money after the purchase"""
    remaining_money = startingMoney - (final_quantity * itemPrice)
    return final_quantity, remaining_money


def new_random_monster():
    """List names that the monster can have"""
    monster_names = ["Golem", "Fire Spirit", "Lava Hound"]
    name = random.choice(monster_names)
    monster = {"name": name}
    
    """Sets description and random stats depending on the monsters name.
    All of them are from clash royale"""
    if name == "Golem":
        monster["description"] = "Slow but durable. When destroyed, explosively splits into two Golemites and deals area damage!"
        monster["health"] = random.randint(80, 120)
        monster["power"] = random.randint(15, 25)
        monster["money"] = random.randint(50, 100)
    elif name == "Fire Spirit":
        monster["description"] = "The Fire Spirit is on a kamikaze mission to give you a warm hug. It'd be adorable if it wasn't on fire.."
        monster["health"] = random.randint(10, 30)
        monster["power"] = random.randint(5, 12)
        monster["money"] = random.randint(200, 400)
    elif name == "Lava Hound":
        monster["description"] = "The Lava Hound is a majestic flying molten beast with obsidian skin and fire breath."
        monster["health"] = random.randint(150, 200)
        monster["power"] = random.randint(30, 45)
        monster["money"] = random.randint(10, 30)
        
    return monster

def print_welcome(name, width):
    """Prints a elcome message
    Parameters: name, width
    Returns: None"""
    print(f"{'Hello, ' + name + '!':^{width}}")

def print_shop_menu(item1Name, item1Price, item2Name, item2Price):
    """Prints a formatted menu.
    Args:
        item1Name (str): First item name.
        item1Price (float): First item price.
        item2Name (str): Second item name.
        item2Price (float): Second item price."""
    p1 = f"${item1Price:.2f}"
    p2 = f"${item2Price:.2f}"
    print(f"| {item1Name:<12}{p1:>9} |")
    print(f"| {item2Name:<12}{p2:>9} |")

def get_user_action(options):
    """Validates user input for game options."""
    while True:
        choice = input("Choice: ")
        if choice in options:
            return choice
        print(f"Invalid choice. Pick from {options}")

def combat(state):
    """Handles fight logic using the state dictionary."""
    monster = new_random_monster()
    m_hp = monster["health"]
    print(f"\n--- BATTLE: {monster['name']} ---")
    
    weapon = next((i for i in state["player_inventory"] if i.get("equipped")), None)
    current_power = state["player_power"] + (20 if weapon else 0)

    while state["player_hp"] > 0 and m_hp > 0:
        print(f"\nYour HP: {state['player_hp']} | {monster['name']} HP: {m_hp}")
        
        has_orb = any(i["name"] == "Magic Orb" for i in state["player_inventory"])
        
        options = ["1", "2"]
        prompt = "Choose your move:\n1) Attack\n2) Run"
        if has_orb:
            options.append("3")
            prompt += "\n3) Use Magic Orb (Instant Win!)"
        
        print(prompt)
        action = get_user_action(options)
        
        if action == "1":
            m_hp -= current_power
            state["player_hp"] -= monster["power"]
            print(f"You deal {current_power} damage!")
        elif action == "3":
            print(f"You used the Magic Orb! The {monster['name']} is defeated instantly!")
            orb = next(i for i in state["player_inventory"] if i["name"] == "Magic Orb")
            state["player_inventory"].remove(orb)
            m_hp = 0
        else:
            print("You escaped!")
            return

    if m_hp <= 0:
        print(f"VICTORY! You found {monster['money']} gold.")
        state["player_gold"] += monster["money"]

def equip_item(state):
    """Filters inventory for weapons and lets the user equip one."""
    weapons = [i for i in state["player_inventory"] if i["type"] == "weapon"]
    
    if not weapons:
        print("\nYou have no weapons to equip!")
        return

    print("\n--- Equip a Weapon ---")
    for idx, w in enumerate(weapons):
        status = "(Equipped)" if w.get("equipped") else ""
        print(f"{idx + 1}) {w['name']} {status}")
    print(f"{len(weapons) + 1}) Unequip All")

    choice = get_user_action([str(i) for i in range(1, len(weapons) + 2)])
    choice = int(choice)

    for w in weapons:
        w["equipped"] = False
    
    if choice <= len(weapons):
        weapons[choice - 1]["equipped"] = True
        print(f"You equipped the {weapons[choice - 1]['name']}!")

import json

def save_game(state, filename="savegame.json"):
    """Saves the player state to a .json file."""
    try:
        save_state = state.copy()
        save_state["monsters"] = [m.to_dict() for m in state["monsters"]]
        with open(filename, "w") as f:
            json.dump(save_state, f, indent=4)
        print(f"Game successfully saved to {filename}.")
    except Exception as e:
        print(f"Error saving game: {e}")

def load_game(filename="savegame.json"):
    import json
    from wanderingmonster import WanderingMonster
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            data["monsters"] = [WanderingMonster.from_dict(d) for d in data["monsters"]]
            print(f"DEBUG: Found file {filename} and loaded data.")
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"DEBUG: Could not find or read {filename}.")
        return None

def move_player(game_state, direction):
    """Updates map_state in place and returns movement result."""
    m_state = game_state["map_state"]
    curr_x, curr_y = m_state["player_pos"]

    """Finds newest position."""
    if direction == "up" and curr_y > 0:
        curr_y -= 1
    elif direction == "down" and curr_y < 9:
        curr_y += 1
    elif direction == "left" and curr_x > 0:
        curr_x -= 1
    elif direction == "right" and curr_x < 9:
        curr_x += 1
    else:
        return "blocked"

    m_state["player_pos"] = [curr_x, curr_y]

    if m_state["player_pos"] == m_state["town_pos"]:
        return "returned_to_town"
    
    return "moved"

def run_map_interface(game_state):
    """Displays the 10x10 map and handles user input for movement."""
    while True:
        m_state = game_state["map_state"]
        
        print("\n" + "="*20)
        for y in range(10):
            row = ""
            for x in range(10):
                char = ". "
                if [x, y] == m_state["player_pos"]:
                    char = "P "
                elif [x, y] == m_state["town_pos"]:
                    char = "T "
                for m in game_state["monsters"]:
                    if m.x == x and m.y == y:
                        char = "M "
                row += char
            print(row)
        print("="*20)
        print("W=Up, A=Left, S=Down, D=Right | Current Pos:", m_state["player_pos"])

        move_map = {"w": "up", "s": "down", "a": "left", "d": "right"}
        action = input("Move: ").lower()
        
        if action in move_map:
            result = move_player(game_state, move_map[action])
            
            p_pos = tuple(m_state["player_pos"])
            for m in game_state["monsters"][:]:
                if (m.x, m.y) == p_pos:
                    return "monster"

            occ = [(mon.x, mon.y) for mon in game_state["monsters"]]
            for m in game_state["monsters"]:
                m.move(occ, [p_pos, tuple(m_state["town_pos"])], 10, 10)

            if result == "returned_to_town":
                return "town"
            elif result == "blocked":
                print("You can't go this way.")
