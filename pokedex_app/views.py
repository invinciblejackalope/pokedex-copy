from django.shortcuts import render
import urllib.request
import urllib, json
import requests
import json
import random

# Renders homepage with appropriate data
# Adds ability effects to each pokemon's original json
def index(request):
    pokemon_list = []
    pokemon = {}
    abilities = {}
    # Currently displays 5 random pokemon
    for i in range(5):
        r = requests.get('https://pokeapi.co/api/v2/pokemon/' + str(random.randint(1,807)))
        pokemon = r.json()
        # For every ability that pokemon has
        for ab in pokemon["abilities"]:
            # Retrieve its effect from the appropriate URL (prvided in the pokemon's json)
            ability_json = requests.get(ab["ability"]["url"]).json()
            # Append it to "abilities"
            abilities[ab["ability"]["name"]] = ability_json["effect_entries"][0]["effect"]
        # Add the data about the pokemon's abilities into the pokemon's json
        pokemon["custom_abilities"] = abilities
        abilities = {}
        pokemon_list.append(pokemon)
    return render(request, 'pokedex_templates/homepage.html', {"data":pokemon_list})

# Renders pokemon_page with appropriate data
# Uses a separate variable called ds to story each pokemon's abilitys' effects
def show_pokemon(request, pokemon):
    s = 'https://pokeapi.co/api/v2/pokemon/' + pokemon
    r = requests.get(s)
    dict = r.json()
    pokemon_abilities = []
    # For every ability that pokemon has
    for ab in dict["abilities"]:
        ability_json = requests.get(ab["ability"]["url"]).json()
        # Append it to "abilities"
        pokemon_abilities.append({ab["ability"]["name"]:ability_json["effect_entries"][0]["effect"]})
    return render(request, 'pokedex_templates/pokemon_page.html', {"data":dict, "ds":pokemon_abilities})
