import random

class Node:
    def __init__(self, name, description, objects=None):
        self.name = name
        self.description = description
        self.objects = objects or {}
        self.connections = {}

    def add_connection(self, direction, node):
        self.connections[direction] = node

class Player:
    def __init__(self, name):
        self.name = name
        self.elements = ["Air"]
        self.current_element = "Air"
        self.stamina = 200
        self.max_hp = 1000
        self.hp = self.max_hp

    def switch_element(self, new_element):
        self.current_element = new_element

    def consume_stamina(self, amount):
        self.stamina -= amount
        if self.stamina < 0:
            self.stamina = 0

class Enemy:
    def __init__(self, name, element):
        self.name = name
        self.element = element
        self.max_hp = 1000
        self.hp = self.max_hp
def create_game():
    #create nodes for different areas
    starting_area = Node("Start", "You are at the starting area.")
    north_area = Node("North", "You moved to the north area.")
    west_area = Node("West", "You moved to the west area.")
    south_area = Node("South", "You moved to the south area.")
    east_area = Node("East", "You moved to the east area.")

    #create connections between areas
    starting_area.add_connection("north", north_area)
    starting_area.add_connection("west", west_area)
    starting_area.add_connection("south", south_area)
    starting_area.add_connection("east", east_area)

    north_area.add_connection("south", starting_area)
    west_area.add_connection("east", starting_area)
    south_area.add_connection("north", starting_area)
    east_area.add_connection("west", starting_area)

    return starting_area

def battle(player, enemy):
    print(f"\nYou encounter a {enemy.name} with {enemy.element} element!")

    while player.hp > 0 and enemy.hp > 0:
        print(f"\nPlayer HP: {player.hp} | {enemy.name} HP: {enemy.hp} | Stamina: {player.stamina}")
        print("\nChoose your action:")
        print("1. Light Attack")
        print("2. Heavy Attack")
        print("3. Switch Element")

        action = input("Enter your choice (1, 2, or 3): ")

        if action == '1':
            if player.stamina >= 5:
                player_damage = calculate_damage(player.current_element, enemy.element, attack_type="light")
                player.consume_stamina(5)
            else:
                print("Not enough stamina for a light attack. Using a default attack.")
                player_damage = calculate_damage(player.current_element, enemy.element, attack_type="default")
        elif action == '2':
            if player.stamina >= 10:
                player_damage = calculate_damage(player.current_element, enemy.element, attack_type="heavy")
                player.consume_stamina(10)
            else:
                print("Not enough stamina for a heavy attack. Using a default attack.")
                player_damage = calculate_damage(player.current_element, enemy.element, attack_type="default")
        elif action == '3':
            switch_element(player)
            continue
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            continue

        enemy_damage = calculate_enemy_damage(enemy.element, player.current_element)

        player.hp -= enemy_damage
        enemy.hp -= player_damage

        print(f"\nYou dealt {player_damage} damage to the {enemy.name}!")
        print(f"The {enemy.name} dealt {enemy_damage} damage to you.")

    if player.hp <= 0:
        print("You were defeated!")
        return False
    else:
        print(f"\nCongratulations! You defeated the {enemy.name}!")
        return True

def calculate_enemy_damage(attacker_element, defender_element):
    #damage multipliers based on element relationships
    element_multipliers = {
        "Air": {"Air": 1, "Earth": 1.5, "Fire": 0.5, "Water": 1},
        "Earth": {"Air": 0.5, "Earth": 1, "Fire": 1, "Water": 1.5},
        "Fire": {"Air": 1, "Earth": 1, "Fire": 1, "Water": 0.5},
        "Water": {"Air": 1, "Earth": 1, "Fire": 1.5, "Water": .5}
    }

    #enemy randomly chooses between light and heavy attack
    attack_type = random.choice(["light", "heavy"])

    #calculate damage based on multipliers and attack type
    damage_multiplier = element_multipliers[attacker_element][defender_element]
    base_damage = {"light": random.randint(40, 60), "heavy": random.randint(80, 120)}
    damage = int(base_damage[attack_type] * damage_multiplier)

    print(f"The {attacker_element} enemy used a {attack_type} attack!")

    return damage

def calculate_damage(attacker_element, defender_element, attack_type="default"):
    #define damage multipliers based on element relationships
    element_multipliers = {
        "Air": {"Air": 1, "Earth": 1.5, "Fire": 0.5, "Water": 1},
        "Earth": {"Air": 0.5, "Earth": 1, "Fire": 1, "Water": 1.5},
        "Fire": {"Air": 1.5, "Earth": 1, "Fire": 1, "Water": 0.5},
        "Water": {"Air": .5, "Earth": 1, "Fire": 1.5, "Water": 1}
    }

    damage_multiplier = element_multipliers[attacker_element][defender_element]
    base_damage = {"light": random.randint(40, 60), "heavy": random.randint(80, 120)}
    damage = int(base_damage[attack_type] * damage_multiplier)   

    return damage

def switch_element(player):
    print("\nChoose an element to switch to:")
    for i, element in enumerate(player.elements, start=1):
        print(f"{i}. {element}")

    choice = input("Enter your choice (1 or 2): ")

    if choice.isdigit() and 1 <= int(choice) <= 2:
        new_element = player.elements[int(choice) - 1]
        player.switch_element(new_element)
        print(f"You switched to {new_element} element.")
    else:
        print("Invalid choice. Please enter 1 or 2.")

def enter_area_and_battle(player, current_area, enemy):
    print(f"\n{current_area.description}")
    choice = input("Enter 'battle' to engage in a battle or 'map' to return to the map: ").lower()
    if choice == "battle":
        battle_result = battle(player, enemy)
        if battle_result:
            print(f"\nCongratulations! You obtained the {enemy.element} element.")
            player.elements.append(enemy.element)
            return True
        else:
            print("YOU DIED")
    elif choice == "map":
        print("\nYou return to the map.")
    else:
        print("Invalid choice. Please enter 'battle' or 'map'.")

    return False

def main():
    player = Player("Player")
    current_area = create_game()

    print("Welcome to the Elemental Adventure Game!")
    print("Your goal is to obtain all the missing elements.")

    #first battle: Water Lord (North)
    if enter_area_and_battle(player, current_area, Enemy("Water Lord", "Water")):
        #second battle: choose between Fire Lord (West) and Earth Lord (East)
        current_area = current_area.connections["south"]  # Move back to starting point
        if enter_area_and_battle(player, current_area, Enemy("Fire Lord", "Fire")):
            current_area = current_area.connections["south"]  # Move back to starting point
            if enter_area_and_battle(player, current_area, Enemy("Earth Lord", "Earth")):
                #final battle: Elemental Master (South)
                current_area = current_area.connections["south"]  # Move to Elemental Master's area
                if enter_area_and_battle(player, current_area, Enemy("Elemental Master", "All")):
                    print("\nCongratulations! You defeated the Elemental Master and mastered all the elements!")
                    print("YOU WIN!")

if __name__ == "__main__":
    main()



