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
    # Currently displays 5 random pokemon
    for i in range(5):
        abilities = {}

        '''requests.get() is a function used to get a response from an API. It returns a QueryDict object, which is like
        a dictionary but made to deal with multiple values for the same key, which some HTML requests respond with. For
        more information, look here: https://docs.djangoproject.com/en/2.2/ref/request-response/'''
        r = requests.get('https://pokeapi.co/api/v2/pokemon/' + str(random.randint(1, 807)))
        pokemon = r.json()  # Converts QueryDict object to json
        # For every ability that pokemon has
        for ab in pokemon["abilities"]:
            '''Retrieve its effect from the appropriate URL. The original JSON has the url for the pokemon's ability
            page, which is why requests.get can be used here.'''
            ability_json = requests.get(ab["ability"]["url"]).json()  # Again, converted to JSON
            # Append it to "abilities"
            abilities[ab["ability"]["name"]] = ability_json["effect_entries"][0]["effect"]
        # Add the data about the pokemon's abilities into the pokemon's json
        pokemon["custom_abilities"] = abilities
        pokemon_list.append(pokemon)
    '''Render renders the html with the information passed to it inserted in the template. This information is whatever
    is in the dictionary passed as the third argument. In this case, pokemon_list is the only information passed.'''
    return render(request, 'pokedex_templates/homepage.html', {"data": pokemon_list})


# Renders pokemon_page with appropriate data (essentially the same as index but with 1 specified pokemon)
# Uses a separate variable called ds to store each pokemon's ability effects
def show_pokemon(request, pokemon):
    s = 'https://pokeapi.co/api/v2/pokemon/' + pokemon
    # As before, these two lines get a QueryDict and convert it to JSON
    r = requests.get(s)
    dictionary = r.json()
    pokemon_abilities = []
    # For every ability that pokemon has
    for ab in dictionary["abilities"]:
        ability_json = requests.get(ab["ability"]["url"]).json()
        # Append it to "abilities"
        pokemon_abilities.append({ab["ability"]["name"]: ability_json["effect_entries"][0]["effect"]})
    # In this case, dictionary and pokemon_abilities are passed to the template
    return render(request, 'pokedex_templates/pokemon_page.html', {"data": dictionary, "ds": pokemon_abilities})
