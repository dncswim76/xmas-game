import os
import sqlite3
import random
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, make_response

#################################################################
## GAME GLOBALS
#################################################################

#player roles
UNASSIGNED=0
NAUGHTY=1
NICE=2

#GAMESTATES
WELCOME=0
VIEW_ROLE=1
COLLABORATE=2
NOMINATE=3
FINAL_VOTE=4

#MAX ROUNDS
MAXIMUM_ROUNDS=3
FINALV = 100

logged_in_users = []
SESSION_ID = 1


#################################################################
## SETUP
#################################################################

app =Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'xmas_game.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
    ))

app.config.from_envvar('XMAS_GAME_SETTINGS', silent=True)


#################################################################
## DATABASE HANDLING
#################################################################

#connects to the database
def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


#returns a handle on the database
def get_db():

    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

#closes the database connection
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

#initializes the database
def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

#initialize database wrapper built into flask
@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('initialized the database')

#given a user's player id, return the name: (first, last)
def get_name_by_player_id(player_id):
    pass

#returns the player id from the user name
def get_player_id_by_username(user_name):
    pass

#returns if the player has joined the game or not
def player_joined_game(player_id):
    pass

#returns if the user name is available for user
def user_name_available(username):
    pass

def validate_user_name(user_name, password):
    pass
        
#enters a new user into the player table of the database
def add_new_user(user_first_name, user_last_name, password, username, phone_number):
    pass

#enters a new player to join the game
def add_new_player(player_id):
    pass

#gets the player role
def get_player_role(player_id):
    pass

#assigns a role to a player
def assign_player_role(player_id, role_number):
    pass

#enters who the player voted for in the given round
def cast_player_vote(player_id, vote_round, vote_player_id):
    pass

#returns the current state of the game
def get_current_state():
    pass

#returns the round of the game
def get_current_round():
    pass

#returns current game number id
def get_current_game_num():
    pass

#updates the game state
def set_current_state(new_state):
    pass

#updates the game round
def set_current_round(new_round):
    pass

#returns a list of player IDs
def get_all_players():
    pass

def get_round_winner(win_round):
    pass

#depending on the round determine who can vote
def get_votable_players():
    pass

#resets player information
def reset_players_table():
    pass

#returns a list of player ids of who was voted for in that round
def get_player_votes(vote_round):
    pass

#returns whether the player voted in that round    
def did_player_vote(player_id, vote_round):
    pass

#enters that the player won that round
def set_player_won_round(winner_id, vote_round):
    pass

#################################################################
## GAME STATE ACTIONS
#################################################################

#moves the game onto the next round
def advance_game_round():

    #get state information from database
    current_state = get_current_state()
    current_round = get_current_round()

    #after welcome stage, assign roles and let user's
    #view their role
    if (current_state == WELCOME):
        assign_roles()
        set_current_state(VIEW_ROLE)
        return

    #once players have viewed their roles allow them to collaborate
    if (current_state == VIEW_ROLE):
        set_current_state(COLLABORATE)
        return

    #once voting is done, then tell users to vote via text
    #and then indicate to nominate
    if (current_state == COLLABORATE):
        send_txt_vote_reminder(current_round)
        set_current_state(NOMINATE)
        return

    #tallies up the votes for the round and then goes to the next round
    #or to the final vote
    if (current_state == NOMINATE):

        #determine the winner of the round
        round_winner = determine_round_winner(current_round)
        set_player_won_round(round_winner, vote_round)
                
        #nomination phase still not over, need to
        #continue to nominate more people
        if (current_round<MAXIMUM_ROUNDS):
            set_current_round(current_round+1)            
            set_current_state(COLLABORATE)
        else:            
            set_current_state(DEBATE_TIME)

        return

    #tells everyone to vote!
    if (current_state == DEBATE_TIME):
        send_txt_vote_reminder(FINALV)
        set_current_state(FINAL_VOTE)
        return

    #tallies up the final vote
    if (current_state == FINAL_VOTE):

        #determine the winner of the round
        game_winner = determine_round_winner(FINALV)
        set_player_won_round(game_winner, FINALV)
        set_current_state(GAME_OVER)
        return

    if (current_state == GAME_OVER):
        new_game()
        set_current_state(WELCOME)
        return

    return

#set up environment with a new game    
def new_game():
    reset_players_table()
    set_current_state(WELCOME)
    set_current_round(1)    
    pass

#################################################################
## GAME HELPER FUNCTIONS
#################################################################

#assigns roles randomly to players.  A max of 20% of the total people
#will be chosen as naughty.  
def assign_roles():

    #returns a list of player ids
    players = get_all_players()
    num_players = len(players)

    num_naughty_players = int(0.2*(num_players))

    i = num_naughty_players
    while(i > 0):

        randint = random.randint(0, len(players)-1)
        player = players.pop(randint)
        assign_player_role(player, NAUGHTY)
        i = i - 1

    for player in players:
        assign_player_role(player, NICE)

#tallies the votes from the round and picks the player with the most
#votes
def determine_round_winner(vote_round):
    pass

#uses twilio API to send a text to all players in the game that it is
#time to vote
def send_txt_vote_reminder():
    pass


def register_logged_in(session_id):
    logged_in_users.append(session_id)

def logged_in(session_id):
    return session_id in logged_in_users

def log_out_session(session_id):
    logged_in_users.remove(session_id)

def make_new_session_id():
    old = SESSION_ID
    SESSION_ID = SESSION_ID + 1
    return old


#################################################################
# GAME VIEW TEMPLATES
#################################################################

@app.route('/')
def index():

    #determine if the user already logged in using a cookie
    session_id = request.cookies.get('session_id')
    if session_id != None and logged_in(int(session_id)):
        return redirect(url_for('join_game'))
    else:
        return redirect(url_for('login_screen'))
        
@app.route('/login', methods=['GET', 'POST'])
def login_screen():

    #if user is already logged in redirect
    session_id = request.cookies.get('session_id')
    if session_id != None and logged_in(int(session_id)):
        return redirect(url_for('index'))

    if request.method == 'POST':
        
        #check the login information to see if it matches information in the database
        user_name = request.form['username']
        password  = request.form['password']
        if (not validate_user_name(user_name, password)):
            flash("Incorrect Username or Password!")
            return redirect(url_for('login_screen'))
                       

        #create a session ID and redirect to normal page
        sessionid = make_new_session_id()
        response = make_response(redirect(url_for('index')))
        register_logged_in(sessionid)
        response.set_cookie('session_id', str(sessionid))
        response.set_cookie('user_name', user_name)
        return response

    #display login screen
    return render_template('login.html')
    
@app.route('/logout')
def logout():
    session_id = request.cookies.get('session_id')                             
    log_out_session(int(session_id))
    return redirect(url_for('index'))

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up_screen():
                                 
    if (request.method == 'POST'):
        #enter new user if username isn't already taken
        username        = request.form['username']
        
        if (not user_name_available(username)):
            flash('User name unavailable')
            return redirect(url_for('sign_up_screen'))

        #make sure passwords are equal
        password1       = request.form['password1']
        password2       = request.form['password2']
        if (password1 != password2):
            flash('unequal passwords')
            return redirect(url_for('sign_up_screen'))
        
        user_first_name = request.form['first_name']
        user_last_name  = request.form['last_name']
        phone_number    = request.form['phone_number']

        add_new_user(user_first_name, user_last_name, password, username, phone_number)
                                
        return redirect(url_for('login_screen'))

    return render_template('sign_up.html')

@app.route('/join')
def join_game():

    #if user is already logged in redirect
    session_id = request.cookies.get('session_id')
    if logged_in(int(session_id)):
        return redirect(url_for('index'))

    #determine the username of the person
    user_name = request.cookies.get('user_name')
    
    #if game is in welcome stage allow players to join
    if   ((get_current_state() == WELCOME) and player_joined_game(get_player_id_by_username(user_name))):
        return render_template('join_game.html')

    #game is in welcome stage but user already joined
    elif ((get_current_state() == WELCOME) and player_joined_game(get_player_id_by_username(user_name))):
        return redirect(url_for('home_screen'))

    #game entrance is closed
    else:
        return render_template('game_closed.html')

@app.route('/joined', methods=['POST'])
def joined_game():
    
    #if user is already logged in redirect
    session_id = request.cookies.get('session_id')
    if logged_in(int(session_id)):
        return redirect(url_for('index'))

    #determine the username of the person
    user_name = request.cookies.get('user_name')

    #if accepting players, log the player else redirect to join screen to indicate
    #we are no longer accepting players
    if ((get_current_state() == WELCOME)):
        add_new_player(get_player_id_by_username(user_name))
    else:
        return redirect(url_for('join_game'))

    return redirect(url_for('home_screen'))
                                 

@app.route('/home_screen')
def home_screen():

    #if user is already logged in redirect
    session_id = request.cookies.get('session_id')
    if not logged_in(int(session_id)):
        return redirect(url_for('index'))

    if (get_current_state() == GAME_OVER):
        winner = get_round_winner(FINALV)
        redner_template('game_over.html', winner=winner)
    
    return render_template('home_screen.html')

@app.route('/my_role')
def my_role_screen():

    #if user is already logged in redirect
    session_id = request.cookies.get('session_id')
    #determine the username of the person
    user_name = request.cookies.get('user_name')
    
    if not logged_in(int(session_id)):
        return redirect(url_for('index'))

    if ((get_current_state()==VIEW_ROLE) and get_player_role(get_player_id_by_username(user_name))==NAUGHTY):
        return render_template('my_role_naughty.html')        
    
    return render_template('my_role.html')

@app.route('/view_players')
def view_players_screen():

    #if user is already logged in redirect
    session_id = request.cookies.get('session_id')
    if not logged_in(int(session_id)):
        return redirect(url_for('index'))

    players = get_all_players()

    return render_template('view_players.html', players=players)


@app.route('/vote', methods=['GET', 'POST'])
def view_vote_screen():

    if (request.method == 'POST'):
        pass
        
    #if user is already logged in redirect
    session_id = request.cookies.get('session_id')
    if logged_in(int(session_id)):
        return redirect(url_for('index'))

    nominees = get_votable_players()

    return render_template('vote_players.html', nominees=nominees)
    

@app.route('/admin')
def admin_screen():

    return render_template('admin.html')

@app.route('/cast_vote/<int:vote_player_id>')
def cast_vote(vote_player_id):

    #if user is already logged in redirect
    session_id = request.cookies.get('session_id')    
    #determine the username of the person
    user_name = request.cookies.get('user_name')
    
    player_id = get_player_id_by_username(user_name)
    
    cast_player_vote(player_id, get_current_round(), vote_player_id)
    return redirect(url_for('view_vote_screen'))

#admin function to advance the game to the next round
@app.route('/advance')
def advance_game():
    advance_game_round()
    return redirect(url_for('admin_screen'))

#reset the game to go to the beginning
@app.route('/reset_game')
def reset_game():
    new_game()
    return redirect(url_for('home_screen'))

#list all the users of the game who have created an account
@app.route('/users')
def list_users_screen():
    return render_template('list_all_players.html')
    

if __name__ == "__main__":
        app.run(host='0.0.0.0', port=33, debug=True)

        
