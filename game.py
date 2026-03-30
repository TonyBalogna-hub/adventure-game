"""
Main game that uses functions from the gamefunction.py.
It will greet the user, display a shop menu, and simulate random monster encounters.
Things have been removed for the updated assignment.
"""
import gamefunctions

def main():
    hp, gold, power = 30, 10, 15
    name = input("Enter your name: ")
    gamefunctions.print_welcome(name, 30)

    while hp > 0:
        print(f"\nTown Square | HP: {hp} | Gold: {gold}")
        print("1) Fight Monster\n2) Sleep (5 Gold)\n3) Quit")
        choice = gamefunctions.get_user_action(["1", "2", "3"])

        if choice == "1":
            hp, earned_gold = gamefunctions.combat(hp, power)
            gold += earned_gold
        elif choice == "2":
            if gold >= 5:
                gold, hp = gold - 5, 30
                print("Restored to 30 HP!")
            else:
                print("Not enough gold!")
        elif choice == "3":
            break

    print(f"Game Over. You Lose Sucker.")

if __name__ == "__main__":
    main()
