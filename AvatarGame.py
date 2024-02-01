import random

class Player:
    def __init__(self, name):
        self.name = name
        self.elements = ["Air"]
        self.current_element = "Air"
        self.stamina = 200
        self.max_hp = 1000
        self.attack = 1
        self.defence = 1
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

def battle(player, enemy):
    print(f"\nYou encounter a {enemy.name} with {enemy.element} element!")

    while player.hp > 0 and enemy.hp > 0:
        print(f"\nPlayer HP: {player.hp} | Stamina: {player.stamina}")
        print(f"\n{enemy.name} HP: {enemy.hp}")
        print("\nChoose your action:")
        print("1. Light Attack")
        print("2. Heavy Attack")
        print("3. Special Attack")
        print("4. Switch Element")

        action = input("Enter your choice (1, 2, 3, 4): ")

        if action == '1':
            if player.stamina >= 5:
                player_damage = calculate_damage(player.current_element, enemy.element, player.attack, attack_type="light")
                player.consume_stamina(5)

                enemy_damage = calculate_enemy_damage(enemy.element, player.current_element, player.defence)

                player.hp -= enemy_damage
                enemy.hp -= player_damage

                print(f"\nYou dealt {player_damage} damage to the {enemy.name}!")
                print(f"The {enemy.name} dealt {enemy_damage} damage to you.")
            else:
                print("Not enough stamina for a light attack. Using a default attack.")
                player_damage = calculate_damage(player.current_element, enemy.element, player.attack, attack_type="default")
        elif action == '2':
            if player.stamina >= 10:
                player_damage = calculate_damage(player.current_element, enemy.element, player.attack, attack_type="heavy")
                player.consume_stamina(10)

                enemy_damage = calculate_enemy_damage(enemy.element, player.current_element, player.defence)

                player.hp -= enemy_damage
                enemy.hp -= player_damage

                print(f"\nYou dealt {player_damage} damage to the {enemy.name}!")
                print(f"The {enemy.name} dealt {enemy_damage} damage to you.")

            else:
                print("Not enough stamina for a heavy attack. Using a default attack.")
                player_damage = calculate_damage(player.current_element, enemy.element, player.attack, attack_type="default")
        elif action == '3':
            if player.stamina >= 20:
                special_attack(player)
                player.consume_stamina(20)

                enemy_damage = calculate_enemy_damage(enemy.element, player.current_element, player.defence)
                player.hp -= enemy_damage
                print(f"\nYou used special attack!")
                print(f"The {enemy.name} dealt {enemy_damage} damage to you.")

        elif action == '4':
            switch_element(player)
            enemy_damage = calculate_enemy_damage(enemy.element, player.current_element, player.defence)
            player.hp -= enemy_damage
            print(f"The {enemy.name} dealt {enemy_damage} damage to you.")
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4.")
            continue

        
    if player.hp <= 0:
        print("You were defeated!")
        return False
    elif player.stamina <= 0:
        print("You passed out!")
        return False
    else:
        print(f"\nCongratulations! You defeated the {enemy.name}!")
        player.attack = 1
        player.defence = 1
        player.hp += 500
        return True

def calculate_enemy_damage(attacker_element, defender_element, defence):
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
    damage = int(base_damage[attack_type] * (defence) * damage_multiplier)

    print(f"The {attacker_element} enemy used a {attack_type} attack!")

    return damage

def calculate_damage(attacker_element, defender_element, attack, attack_type="default"):
    #define damage multipliers based on element relationships
    element_multipliers = {
        "Air": {"Air": 1, "Earth": 1.5, "Fire": 0.5, "Water": 1},
        "Earth": {"Air": 0.5, "Earth": 1, "Fire": 1, "Water": 1.5},
        "Fire": {"Air": 1.5, "Earth": 1, "Fire": 1, "Water": 0.5},
        "Water": {"Air": .5, "Earth": 1, "Fire": 1.5, "Water": 1}
    }

    damage_multiplier = element_multipliers[attacker_element][defender_element]
    base_damage = {"light": random.randint(40, 60), "heavy": random.randint(80, 120)}
    damage = int(base_damage[attack_type] * attack * damage_multiplier)

    return damage

def special_attack(player):
    if player.current_element == 'Air':
        player.stamina += 100
    if player.current_element == 'Water':
        if player.hp <= player.max_hp-100:
            player.hp += 100
        else:
            player.hp = player.max_hp
    if player.current_element == 'Earth':
        player.defence * .8
    if player.current_element == 'Fire':
        player.attack * 1.2
        
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

def battle(player, enemy):
    battle_result = battle(player, enemy)
    if battle_result:
        print(f"\nCongratulations! You obtained the {enemy.element} element.")
        player.elements.append(enemy.element)
        return True
    else:
        print("YOU DIED")

    return False

def main():
    player = Player("Player")

    print("Welcome to the Elemental Adventure Game!")
    print("Your goal is to obtain all the missing elements by defeating the Lords of the other nations.")

    print("Press enter to start")
    input()

    #first battle: Water Lord (North)
    if battle(player, Enemy("Water Lord", "Water")):
        #second battle: choose between Fire Lord (West) and Earth Lord (East)
        if battle(player, Enemy("Fire Lord", "Fire")):
            if battle(player, Enemy("Earth Lord", "Earth")):
                #final battle: Elemental Master (South)
                if battle(player, Enemy("Elemental Master", "All")):
                    print("\nCongratulations! You defeated the Elemental Master and mastered all the elements!")
                    print("YOU WIN!")

if __name__ == "__main__":
    main()



