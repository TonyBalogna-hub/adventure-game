# Name: Antonio [Your Last Name]
# Date: February 22, 2026
# gamefunctions.py

import random

def purchase_item(itemPrice, startingMoney, quantityToPurchase=1):
    # Calculate how many items you can afford with start money
    affordable_quantity = startingMoney // itemPrice
    # Limits the purchase to the requested amount or what is affordable
    final_quantity = min(quantityToPurchase, affordable_quantity)
    # Calculates the remaining money after the purchase
    remaining_money = startingMoney - (final_quantity * itemPrice)
    return final_quantity, remaining_money


def new_random_monster():
    # List names that the monster can have
    monster_names = ["Golem", "Fire Spirit", "Lava Hound"]
    name = random.choice(monster_names)
    monster = {"name": name}
    
    # Sets description and random stats depending on the monsters name, All of them are from clash royale
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

# Call purchase_item three times with different inputs
num, money = purchase_item(341, 2112)
print(f"Bought: {num}, Left: {money}")

num, money = purchase_item(123, 201, 3)
print(f"Bought: {num}, Left: {money}")

num, money = purchase_item(100, 1000, 5)
print(f"Bought: {num}, Left: {money}")

# Call new_random_monster three different times
m1 = new_random_monster()
print(m1)

m2 = new_random_monster()
print(m2)

m3 = new_random_monster()
print(m3)

def print_welcome(name, width):
    """
    Prints a elcome message
    Parameters: name, width
    Returns: None
    """
    print(f"{'Hello, ' + name + '!':^{width}}")

def print_shop_menu(item1Name, item1Price, item2Name, item2Price):
    """
    Prints menu.
    Parameters: item1Name, item1Price, item2Name, item2Price
    Returns: None
    """
    p1 = f"${item1Price:.2f}"
    p2 = f"${item2Price:.2f}"
    print(f"| {item1Name:<12}{p1:>9} |")
    print(f"| {item2Name:<12}{p2:>9} |")
   
# Call print_welcome three times
print_welcome("Jeff", 20)
print_welcome("Tony", 20)
print_welcome("Antonio", 23)

# Call print_shop_menu three times
print_shop_menu("Stew", 8, "Bread", 3)
print_shop_menu("Staff", 150, "Satchel", 30)
print_shop_menu("Sword", 150, "Shield", 90)

input("\nPress Enter to exit...")
