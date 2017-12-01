from flask import flash, g, jsonify, redirect, render_template, request, session, url_for
from sqlalchemy import text
from xmas_game import app, db

from .models import Setting, Round, User, Vote, Player

from flask_login import login_user, logout_user, current_user, login_required
from xmas_game import app, db, login_manager

from .forms import AccountCreateForm, LoginForm
from .models import User


@app.before_request
def before_request():
    g.user = current_user

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    ''' User login page.'''

    # make sure that user is not already logged in
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('home'))
    # instantiate LoginForm
    form = LoginForm()
    # process form submission on POST
    if form.validate_on_submit():
        session['user_id'] = form.user.id
        session['authenticated'] = True
        # check if user has access to next url
        next = request.args.get('next')
        return redirect(next or url_for('home'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    ''' User logout page.'''
    
    logout_user()
    # pop session variables
    session.pop('user_id', None)
    session.pop('authenticated', None)
    return redirect(url_for('home'))


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    ''' Account creation page.'''

    form = AccountCreateForm(request.form)
    if form.validate_on_submit():
        user = User(
                username=form.username.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('create_account.html', form=form) 


@app.route('/')
@app.route('/home')
def home():

    #Home Screen Lists the current game state and the nominees from the
    #first round.  It will also show the final winner of the game and
    #indicate if they are naughty or nice

    if not current_user.is_authenticated:        
        return redirect(url_for('login'))    
    else:

        player_joined = Player.query.filter(Player.user_id==current_user.id).first()!=None
        game_state_setting = Setting.query.filter(Setting.config_var=='game_state')[0]
        
        return render_template('home.html',
                               game_state_setting=game_state_setting, 
                               player_joined=player_joined)

@app.route('/join_game')
def join_game():
                             
    player_joined = Player.query.filter(Player.user_id==current_user.id).first()!=None
    
    if not player_joined:      
        new_player = Player(user_id=current_user.id, role=Player.Roles.UNASSIGNED)
        db.session.add(new_player)
        db.session.commit()
    
    return redirect(url_for('home'))


@app.route('/view_players')
def view_players():

    #takes to a screen where all players are lists, and also indicates
    #if each player has cast their vote for each voting session yet
    #or not
    all_players = Player.query.all()
    return render_template('view_players.html', players=all_players)


@app.route('/my_role')
def my_role():

    #indicates the players role when the game allows players to view their roles
    #a role can be naughty or nice.  Naughty people will be shown a list of other
    #naughty people.  IF the game doesn't let people view a role, then the screen
    #indicates that the role viewing period has ended
    pass


@app.route('/vote')
def vote():

    #GET - lists all people available to select for this voting round. The users can only select
    #one person to cast a vote for.
    #POST - send the id of the person they are voting for
    pass
