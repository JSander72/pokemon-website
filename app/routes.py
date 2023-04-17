from flask import redirect, render_template, request, session, url_for
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
                        session['poke_dict'] =  poke_dict

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
def capture():
    print("we made it to the capture function")
    poke_dict = session.get('poke_dict', None)
    print("We have the poke_dict variable in capture()")
    if poke_dict is None:
        print('Something is wrong with session.get("poke_dict")')
        return redirect(url_for('poke'))
    
    elif poke_dict != None:
        print("We are successfully using the poke_dict in the capture function")
        id = poke_dict['poke_id']
        name = poke_dict['name']
        attack = poke_dict['attack base stat']
        defense = poke_dict['defense stat']
        hp = poke_dict['hp base stat']
        exp = poke_dict['base experience']
        type1 = poke_dict['type1']
        type2 = poke_dict['type2']
        poke_img = poke_dict['photo']


        #add upokemon to database
        pokemon = Pokemon(id, name, attack, defense, hp , exp, type1, type2, poke_img)
        print(pokemon)
        pokemon.saveToDB()
        print(f'Succesfully stored {name}!')
        return redirect(url_for('poke'))
    else:
        print('Something is still not right')

@app.route('/profile')
def profilePage():
    return render_template('profile.html')

