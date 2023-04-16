from flask import redirect, render_template, request, url_for
from app import app
from .forms import PokeDex
import requests as r
from .models import Pokemon
from flask_login import login_required

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/pokedex', methods=['GET', 'POST'])
def poke():
    form = PokeDex()
    # if form.is_submitted():
    #     result = request.form
    #     return render_template('pokedex.html', result=result)
    
    if request.method == 'POST':
        if form.validate():
            pokereq = form.pokereq.data #name of pokemon requested from user
            try:
                 pokemon = r.get(f"https://pokeapi.co/api/v2/pokemon/{int(pokereq)}/")
            except:
                pokemon = r.get(f"https://pokeapi.co/api/v2/pokemon/{pokereq.lower()}/")

            if pokemon.ok:

                data = pokemon.json()
                for pokemon in data:
                    try:
                        poke_dict={}
                        poke_dict={
                                "poke_id": data['id'],
                                "name": data['name'].title(),
                                "ability1":data['abilities'][0]["ability"]["name"],
                                "ability2": data['abilities'][1]["ability"]["name"] if len(data['abilities']) >= 2 else "" ,
                                "base experience":data['base_experience'],
                                "photo":data['sprites']['other']['home']["front_default"],
                                "attack base stat": data['stats'][1]['base_stat'],
                                "hp base stat":data['stats'][0]['base_stat'],
                                "defense stat":data['stats'][2]["base_stat"],
                                "type1":data['types'][0]["type"]['name'],
                                "type2": data['types'][1]["type"]['name'] if len(data['types']) >= 2 else ""}
                        capture_poke = poke_dict

                    except:
                        print('An empty form was submitted!')
                        return redirect(url_for('poke'))
                return render_template('pokedex.html', form=form, poke_dict=poke_dict)
                #return render_template('pokedex.html', form=form, pokereq=pokereq)
            else:
                print("Error with pokemon.ok")
                return render_template('pokedex.html', form=form)


    return render_template('pokedex.html', form=form)


@app.route('/capture', methods=("GET", "POST"))
@login_required
def capture(capture_poke):
    print("we made it to the capture function")
    if request.method == 'POST':
        print("We also made it to the actual POST method")
        id = capture_poke['poke_id']
        name = capture_poke['name']
        attack = capture_poke['attack base stat']
        defense = capture_poke['defense stat']
        hp = capture_poke['hp base stat']
        exp = capture_poke['base experience']
        type1 = capture_poke['type1']
        type2 = capture_poke['type2']
        poke_img = capture_poke['photo']


        #add upokemon to database
        pokemon = Pokemon(id, name, attack, defense, hp , exp, type1, type2, poke_img)
        print(pokemon)
        pokemon.saveToDB()
        print(f'Succesfully stored {pokemon}!')
        pass


