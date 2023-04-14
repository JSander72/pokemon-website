from flask import redirect, render_template, request, url_for
from app import app
from .forms import PokeDex, SignUpForm
import requests as r
from .models import User

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
                            "ability2": data['abilities'][1]["ability"]["name"] if len(data['abilities']) >= 2 else "" ,
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

@app.route('/signup', methods=["GET", "POST"])
def signUp():
    form = SignUpForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            password = form.password.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            
            #add user to database
            user = User(username, password, first_name, last_name, email)
            print(user)
            user.saveToDB()
            print(user)
            return redirect(url_for('poke'))


    return render_template('signup.html', form = form)