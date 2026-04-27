"""
Main game that uses functions from the gamefunction.py.
It will greet the user, display a shop menu, and simulate random monster encounters.
Things have been removed, changed, or added for the updated assignment.
"""
import gamefunctions
import random
from wanderingmonster import WanderingMonster

def main():
    print("--- ADVENTURE GAME ---")
    print("1) New Game\n2) Load Game")
    start_choice = gamefunctions.get_user_action(["1", "2"])

    if start_choice == "2":
        state = gamefunctions.load_game()
        if state:
            print(f"Welcome back, {state['player_name']}!")
        else:
            print("Starting new game instead")
            start_choice = "1"
    
    if start_choice == "1":
        state = {
            "player_name": "Antonio",
            "player_hp": 100,
            "player_gold": 1000, 
            "player_power": 15,
            "player_inventory": [],
            "map_state": {
                "player_pos": [0, 0],
                "town_pos": [0, 0]
            },
            "monsters": []
        }

        for _ in range(1):
            m = WanderingMonster.random_spawn([], 
                [tuple(state["map_state"]["player_pos"]), tuple(state["map_state"]["town_pos"])], 10, 10)
            state["monsters"].append(m)

        gamefunctions.print_welcome(state["player_name"], 30)
    
    """Main game loop"""
    while state["player_hp"] > 0:
        print(f"\n--- TOWN ---")
        print(f"HP: {state['player_hp']} | Gold: {state['player_gold']}")
        print("1) Explore Map\n2) Visit Shop\n3) Equip Weapon\n4) Save and Quit")
        
        choice = gamefunctions.get_user_action(["1", "2", "3", "4"])

        if choice == "1":
            result = gamefunctions.run_map_interface(state)
            
            if result == "monster":
                gamefunctions.combat(state) 
                
                p_pos = tuple(state["map_state"]["player_pos"])
                for m in state["monsters"][:]:
                    if (m.x, m.y) == p_pos:
                        state["monsters"].remove(m)
                
                if len(state["monsters"]) == 0:
                    for _ in range(2):
                        new_m = WanderingMonster.random_spawn([], 
                            [p_pos, tuple(state["map_state"]["town_pos"])], 10, 10)
                        state["monsters"].append(new_m)
        
        elif choice == "2" or choice == "3":
            """Shop logic updated with the old sleep mechanic (accidentally removed) and tracks map state."""
            if state["map_state"]["player_pos"] == state["map_state"]["town_pos"]:
                if choice == "2":
                    print("\n--- SHOP ---")
                    gamefunctions.print_shop_menu("Sword", 150, "Magic Orb", 200)
                    print("1) Buy Sword\n2) Buy Magic Orb\n3) Sleep (5 Gold)\n4) Leave")
                    shop_choice = gamefunctions.get_user_action(["1", "2", "3", "4"])
                    
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

                    elif shop_choice == "3":
                        if state["player_gold"] >= 5:
                            state["player_gold"] -= 5
                            state["player_hp"] = 100
                            print(f"Restored to {state['player_hp']} HP!")
                        else:
                            print("Not enough gold to sleep!")
                    
                    elif shop_choice == "4":
                        print("Returning to town...")

                elif choice == "3":
                    gamefunctions.equip_item(state)
            else:
                print("\n[!] You must be in Town (0,0) to use the Shop or Equip items!")

        elif choice == "4":
            print("Attempting to save...")
            gamefunctions.save_game(state, "savegame.json")
            print("Goodbye, Antonio!")
            break

    if state["player_hp"] <= 0:
        print(f"Game Over. You Lose Sucker.")

if __name__ == "__main__":
    main()
