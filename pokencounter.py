from pprint import pprint
import random
from pokeload import gotta_catch_em_all

def get_player_profile(pokemon_list):
    return {
        "player_name": input("What's your name? "),
        "pokemon_inventory": [random.choice(pokemon_list) for every_pok in range(3)], # es un for mini, se ejecuta la acción que menciona primero para el for de después
        "combats": 0,
        "pokeballs": 0,
        "health_potion": 0
    }

def any_player_pokemon_lives(player_profile):
    return sum([pokemon["current_health"] for pokemon in player_profile["pokemon_inventory"]]) > 0

def choose_pokemon(player_profile):
    print("Choose your Pokemon!")
    choosen = None
    while not choosen:
        for index in range(len(player_profile["pokemon_inventory"])):
            print("{} - {}".format(index, pokemon_info(player_profile["pokemon_inventory"][index])))
        try:
            return player_profile["pokemon_inventory"][int(input("Which one do you choose?"))]
            choosen = True
        except (ValueError, IndexError):
            print("Invalid option")



def fight(player_profile, enemy_pokemon):
    print("--- NEW FIGHT ---")
    attack_history = []
    player_pokemon = choose_pokemon(player_profile)
    
    print("{} VS {}".format(pokemon_info(player_pokemon),pokemon_info(enemy_pokemon)))
    
    while any_player_pokemon_lives(player_profile) and enemy_pokemon["current_health"] > 0:
        action = None
        while action not in ["A", "P", "H", "C"]:
            action = input("Choose an action: [A]ttack, [P]okeball, Potion [H]ealth, [C]hange")
        if action == "A":
            player_attack(player_pokemon, enemy_pokemon)
            attack_history.append(player_pokemon)
            enemy_attack(enemy_pokemon, player_pokemon)
        elif action == "P":
            # If user has pokeball, user try to catch the pokemon relative to the health of the enemy
            capture_pokemon(player_profile, player_pokemon)
        elif action == "H":
            # If user has potions, he can cure the pokemon, max 100HP
            cure_pokemon(player_profile, player_pokemon)
        elif action == "C":
            # User can change his pokemon to another on his inventory
            pass
        
        if player_pokemon["current_health"] == 0 and any_player_pokemon_lives(player_profile) > 0:
            player_pokemon = choose_pokemon(player_profile)
    
    if enemy_pokemon["current_health"] == 0:
        print("You WIN!")
        assign_experience(attack_history)
    
    print("--- FIGHT FINISHED ---")
    input("Press any key to continue...")

def assign_experience(attack_history):
    for pokemon in attack_history:
        points = random.randint(1, 5)
        pokemon["current_exp"] += points
        while pokemon["current_exp"] > 20:
            pokemon["current_exp"] -= 20
            pokemon["current_health"] = pokemon["base_health"]
            pokemon["level"] += 1
            print("Your Pokemon has just level up to level {}!".format(pokemon_info(pokemon)))

def player_attack(player_pokemon, enemy_pokemon):
    print("Choose the attack: ")
    # Hay que hacer una comparación para ver fortalezas por tipo
    choosen = None
    while not choosen:
        for index in range(len(player_pokemon["attacks"])):
            print("{} - {}".format(index, pokemon_info(player_pokemon["attacks"][index])))
        try:
            return player_pokemon["player_pokemon"][int(input("Which one do you choose?"))]
        except (ValueError, IndexError):
            print("Invalid option")

def enemy_attack(enemy_pokemon, player_pokemon):
    pass

def pokemon_info(pokemon):
    return "{} | lvl {} | HP {}/{}".format(pokemon["name"],pokemon["level"],pokemon,["current_health"],pokemon["base_health"])

def main():
    pokemon_list = gotta_catch_em_all()
    player_profile = get_player_profile(pokemon_list)
    while any_player_pokemon_lives(player_profile):
        enemy_pokemon = random.choice(pokemon_list)
        fight(player_profile, enemy_pokemon)
        
    print("Has perdido en tu combate #{}".format(player_profile["combats"]))
    

if __name__ == "__main__":
    main()
    
