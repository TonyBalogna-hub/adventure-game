"""
Main game that uses functions from the gamefunction.py.
It will greet the user, display a shop menu, and simulate random monster encounters.
Things have been removed, changed, or added for the updated assignment.
"""
import gamefunctions

def main():
    """Main game state."""
    state = {
        "player_name": "Antonio",
        "player_hp": 100,
        "player_gold": 1000, 
        "player_power": 15,
        "player_inventory": [] 
    }

    gamefunctions.print_welcome(state["player_name"], 30)
    """Main game loop"""
    while state["player_hp"] > 0:
        print(f"\n--- TOWN ---")
        print(f"HP: {state['player_hp']} | Gold: {state['player_gold']}")
        print("1) Fight Monster\n2) Visit Shop\n3) Equip Weapon\n4) Quit")
        
        choice = gamefunctions.get_user_action(["1", "2", "3", "4"])

        if choice == "1":
            gamefunctions.combat(state)
        
        elif choice == "2":
            """Shop logic"""
            print("\n--- SHOP ---")
            gamefunctions.print_shop_menu("Sword", 150, "Magic Orb", 200)
            print("1) Buy Sword\n2) Buy Magic Orb\n3) Leave")
            
            shop_choice = gamefunctions.get_user_action(["1", "2", "3"])
            
            if shop_choice == "1":
                num, remaining = gamefunctions.purchase_item(150, state["player_gold"])
                if num > 0:
                    state["player_gold"] = remaining
                    state["player_inventory"].append({
                        "name": "Sword", 
                        "type": "weapon", 
                        "equipped": False
                    })
                    print("You bought a Sword!")
                else:
                    print("Not enough gold!")

            elif shop_choice == "2":
                num, remaining = gamefunctions.purchase_item(200, state["player_gold"])
                if num > 0:
                    state["player_gold"] = remaining
                    state["player_inventory"].append({
                        "name": "Magic Orb", 
                        "type": "special"
                    })
                    print("You bought a Magic Orb!")
                else:
                    print("Not enough gold!")

        elif choice == "3":
            """Equip logic."""
            gamefunctions.equip_item(state)
            
        elif choice == "4":
            print("Goodbye, Antonio!")
            break

if __name__ == "__main__":
    main()
