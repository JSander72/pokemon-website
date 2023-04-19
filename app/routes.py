from flask import flash, redirect, render_template, request, session, url_for
from app import app
from .forms import PokeDex
import requests as r
from .models import MyPokemon, Pokemon, TeamPokemon, Teams, User
from flask_login import login_required, current_user

@app.route('/')
def home():
    return render_template('index.html')

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
    poke_dict = session.get('poke_dict', None)

    if poke_dict is None:
        print('Something is wrong with session.get("poke_dict")')
        return redirect(url_for('poke'))
    
    elif poke_dict != None:
        id = poke_dict['poke_id']
        name = poke_dict['name']
        attack = poke_dict['attack base stat']
        defense = poke_dict['defense stat']
        hp = poke_dict['hp base stat']
        exp = poke_dict['base experience']
        type1 = poke_dict['type1']
        type2 = poke_dict['type2']
        poke_img = poke_dict['photo']
        ability1 = poke_dict['ability1']
        ability2 = poke_dict['ability2']

        #add pokemon to database

        pokemon = Pokemon(id, name, attack, defense, hp , exp, type1, type2, poke_img, ability1, ability2)
        existing_pokemon = Pokemon.query.filter_by(id=id).first()
        if existing_pokemon is None:
            pokemon.saveToDB()
            flash(f'Succesfully stored {name}!', 'success')

            #store pokemon in mypokemon
            to_capture = MyPokemon(current_user.id, id )
            print(to_capture)
            to_capture.saveToDB()
            print(f'You captured {name}!!')
        else:
            to_capture = MyPokemon(current_user.id, id )
            print(f"to_capture already in Pokemon table")
            to_capture.saveToDB()
            print(f'You captured {name}!!')

        return redirect(url_for('poke'))
    else:
        print('Something is still not right')


@app.route('/training')
@login_required
def pokeTeams():
    user = User.query.filter_by(id=current_user.id).first()
    mypokemons = MyPokemon.query.filter_by(user_id=user.id).all()
    return render_template('training.html', mypokemons=mypokemons)