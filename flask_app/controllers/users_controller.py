from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_bcrypt import Bcrypt
from flask_app.models.user_model import User
from flask_app.models.shows_model import Show

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/users/register', methods=['POST'])
def register():
    if not User.validate(request.form):
        return redirect('/')
    hashed_pass = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password': hashed_pass
    }
    id = User.create(data)
    session['user_id'] = id
    
    return redirect('/welcome')


@app.route('/users/login', methods=['POST'])
def login():
    data = {'email' : request.form['email']}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash('Invalid login info', 'log')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid login info', 'log')
        return redirect('/')
    session['user_id'] = user_in_db.id
    session['email'] = request.form['email']
    return redirect('/welcome')


@app.route('/welcome')
def welcome():
    if 'user_id' not in session:
        return redirect('/')
    all_shows = Show.get_all()
    user_data = {
        'id': session['user_id'],
        'email': session['email']
    }
    user = User.get_by_email(user_data)
    return render_template('welcome.html', user=user, all_shows=all_shows)

@app.route('/users/logout')
def logout():
    del session['user_id']
    return redirect('/')