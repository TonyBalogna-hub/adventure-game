"""
Main game that uses functions from the gamefunction.py.
It will greet the user, display a shop menu, and simulate random monster encounters.
"""
import gamefunctions

def main():
    name = input("Enter your character name: ")
    gamefunctions.print_welcome(name, 30)
    
    print("\nYou enter a shop...")
    gamefunctions.print_shop_menu("Potion", 10.5, "Antidote", 5.0)
    
    # Example interaction
    qty, change = gamefunctions.purchase_item(10.5, 50, 2)
    print(f"You bought {qty} Potions. Change: ${change:.2f}")
    
    print("\nSomething attacks!")
    monster = gamefunctions.new_random_monster()
    print(f"A {monster['name']} appeared! {monster['description']}")

if __name__ == "__main__":
    main()
