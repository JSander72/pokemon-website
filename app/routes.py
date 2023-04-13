from flask import redirect, render_template, request, url_for
from app import app
from .forms import PokeDex
import requests as r

@app.route('/')
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
                    poke_dict={}
                    poke_dict={
                            "poke_id": data['id'],
                            "name": data['name'].title(),
                            "ability1":data['abilities'][0]["ability"]["name"],
                            "ability2":data['abilities'][1]["ability"]["name"],
                            "base experience":data['base_experience'],
                            "photo":data['sprites']['other']['home']["front_default"],
                            "attack base stat": data['stats'][1]['base_stat'],
                            "hp base stat":data['stats'][0]['base_stat'],
                            "defense stat":data['stats'][2]["base_stat"]}
                return render_template('pokedex.html', form=form, poke_dict=poke_dict)
                #return render_template('pokedex.html', form=form, pokereq=pokereq)
            else:
                print("Error with pokemon.ok")
                return render_template('pokedex.html', form=form)


    return render_template('pokedex.html', form=form)

