from requests_html import HTMLSession
import pickle

pokemon_base = {
    "name": "",
    "current_health": 100,
    "base_health": 100,
    "level": 1,
    "type": None,
    "current_exp": 0,
    "attacks": None
}

URL_BASE = "https://www.pokexperto.net/index2.php?seccion=nds/nationaldex/movimientos_nivel&pk="
NUM_POK = 25

def get_pokemon(index):
    url = "{}{}".format(URL_BASE, index)
    session = HTMLSession()
    
    new_pokemon = pokemon_base.copy()
    pokemon_page = session.get(url)
    
    new_pokemon["name"] = pokemon_page.html.find(".mini", first=True).text.split("\n", 1)[0]
    
    new_pokemon["type"] = []
    for el_img in pokemon_page.html.find(".pkmain", first=True).find(".bordeambos", first=True).find("img"):
        new_pokemon["type"].append(el_img.attrs["alt"])
    
    new_pokemon["attacks"] = []
    for attack_item in pokemon_page.html.find(".pkmain")[-1].find("tr .check3"):
        attack = {
            "name": attack_item.find("td .nav6c")[1].text,
            "type": attack_item.find("img")[0].attrs["alt"],
            "min_level": attack_item.find(".bazul")[0].find(".center")[0].text,
            "damage": int(attack_item.find(".center")[4].text.replace("--", "0"))
        }
        if attack["damage"] != 0:
            new_pokemon["attacks"].append(attack)
    
    return new_pokemon

def gotta_catch_em_all():
    try:
        print("Loading pokedex...")
        with open("pokedex.pkl", "rb") as pokedex:
            all_pokemons = pickle.load(pokedex)
        if len(all_pokemons) != NUM_POK:
            raise FileNotFoundError
    except FileNotFoundError:
        print("Data not found, loading from website...")
        all_pokemons = []
        for index in range(NUM_POK):
            all_pokemons.append(get_pokemon(index + 1))
            print("*", end="")
        print("\nPokedex loaded")
        with open("pokedex.pkl", "wb") as pokedex:
            pickle.dump(all_pokemons, pokedex)
            
    return all_pokemons
