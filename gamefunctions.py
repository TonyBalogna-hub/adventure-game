# Name: Antonio Hedgpeth
# Date: February 22, 2026
# gamefunctions.py

"""Module for the game functions.

This provides necessary functions for managing the menus,
basic commands, and generation of random monster encounters."""
import random

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
