from flask import Blueprint, flash, get_flashed_messages, redirect, render_template, request, url_for
from .forms import LogIn, SignUpForm
from ..models import User, Pokemon
from flask_login import current_user, login_user, logout_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods=["GET", "POST"])
def signUp():
    form = SignUpForm()
    if request.method == 'POST':
        if form.validate():
            username = form.username.data
            password = form.password.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            #add flash message her for when user already exists
            #if User 
            #add user to database
            user = User(username, password, first_name, last_name, email)
            print(user)
            user.saveToDB()
            print(user)
            return redirect(url_for('auth.loginPage'))

    return render_template('signup.html', form = form)

@auth.route('/login', methods=["GET", "POST"])
def loginPage():
    form = LogIn()
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            password = form.password.data

            user = User.query.filter_by(username=username).first()            
            if user:
                # verify password
                if user.password == password:
                    login_user(user)
                    return redirect(url_for('index'))
                else:
                    print('invalid password')
            else:
                print('incorrect username or password')

    return render_template('login.html', form = form)

@auth.route('/logout')
@login_required
def logMeOut():
    logout_user()
    flash("You've successfully been logged out!", 'success')
    return redirect(url_for('auth.loginPage'))

@auth.route('/myaccount')
def profilePage():

    return render_template('myaccount.html')

@auth.route('/deleteme', methods=["GET"])
@login_required
def deleteUser():

    user = User.query.get_or_404(current_user.id)
    user.deleteFromDB()
    flash("Delete user successful!!", 'success')
    return redirect(url_for('index'))

@auth.route('/deleteme', methods=["GET"]) #Just for me to get rid of pokemon
def deletePokemon():
    # query all pokemon and delete them
    Pokemon.query.delete()
    
    # commit the changes to the database
    db.session.commit()

    return redirect(url_for('index'))