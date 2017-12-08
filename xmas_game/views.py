from flask import flash, g, jsonify, redirect, render_template, request, session, url_for
from sqlalchemy import text
from xmas_game import app, db

from .models import Setting, User, Vote, Player
from .utils import *

from flask_login import login_user, logout_user, current_user, login_required
from xmas_game import app, db, login_manager

from .forms import AccountCreateForm, LoginForm


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

        player_joined = Player.query.filter(Player.user_id==current_user.id).first() is not None
        # this could be an error if the setting does not exist..
        game_state_setting = get_game_state()
        game_round_setting = get_game_round()

        round_winners = [None, None, None, None]
        round_winners[0] = determine_round_winner(1)
        round_winners[1] = determine_round_winner(2)
        round_winners[2] = determine_round_winner(3)
        round_winners[3] = determine_round_winner(4)
        if round_winners[3] != None:
            winner_is_naughty = round_winners[3].role==Player.Roles.NAUGHTY
        else:
            winner_is_naughty = False
            
        return render_template('home.html',
                               game_state_setting=game_state_setting,
                               game_round_setting=game_round_setting, 
                               player_joined=player_joined,
                               round_winners=round_winners,
                               winner_is_naughty=winner_is_naughty)

@app.route('/join_game')
def join_game():
                             
    player_joined = Player.query.filter(Player.user_id==current_user.id).first() is not None
    
    if not player_joined:      
        new_player = Player(user_id=current_user.id,
                            role=Player.Roles.NICE, 
                            voted_round_one="", 
                            voted_round_two="", 
                            voted_round_three="", 
                            voted_round_four="")
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

    player_joined = Player.query.filter(Player.user_id==current_user.id).first() is not None
    if (not player_joined):
        return redirect(url_for('home'))

    #find the player who is requesting his role
    cur_player_naughty = Player.query.filter(Player.user_id==current_user.id).first().role==Player.Roles.NAUGHTY
    naughty_players = Player.query.filter(Player.role==Player.Roles.NAUGHTY)
    game_state = get_game_state()
    
    return render_template('my_role.html', cur_player_naughty=cur_player_naughty,
                                           naughty_players=naughty_players,
                                           game_state=game_state)


@app.route('/vote', methods=['GET', 'POST'])
def vote():

    #GET - lists all people available to select for this voting round. The users can only select
    #one person to cast a vote for.
    #POST - send the id of the person they are voting for
    
    player_joined = Player.query.filter(Player.user_id==current_user.id).first() is not None
    if (not player_joined):
        return redirect(url_for('home'))

    if (request.method == "POST"):

        voted_for_player_id = int(request.form["selected"])
        voter_player_id = Player.query.filter(Player.user_id==current_user.id).first().id
        vote_round = int(get_game_round())
        cast_vote(voter_player_id, voted_for_player_id, vote_round)

        return redirect(url_for('home'))
    
    game_state_setting = get_game_state()
    game_round_setting = get_game_round()

    round1_winner = determine_round_winner(1)
    round2_winner = determine_round_winner(2)
    round3_winner = determine_round_winner(3)

    if (game_round_setting != "4"):
        votable_players = Player.query.all()
        if (round1_winner != None and int(game_round_setting) > 1):
            votable_players.remove(determine_round_winner(1))
        if (round2_winner != None and int(game_round_setting) > 2):
            votable_players.remove(determine_round_winner(2))
    else:
        votable_players = [round1_winner, round2_winner, round3_winner]
        
    return render_template('vote.html',
                           votable_players=votable_players,
                           game_state_setting=game_state_setting,
                           game_round_setting=game_round_setting)


@app.route('/advance_game')
def advance_game():
    if current_user.username == "dncswim76":
        advance_the_game()
    return redirect(url_for('home'))

@app.route('/new_game')
def new_game():

    if current_user.username == "dncswim76":
        start_new_game()
    return redirect(url_for('home'))

#quick hack for admin game controller
@app.route('/admin_dave')
def admin_dave():
    if current_user.username == "dncswim76":
           return render_template('admin_dave.html')
    return redirect(url_for('home'))
