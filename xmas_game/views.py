from flask import flash, g, jsonify, redirect, render_template, request, session, url_for


@app.route('/')
@app.route('/home')
def home():

    #Home Screen Lists the current game state and the nominees from the
    #first round.  It will also show the final winner of the game and
    #indicate if they are naughty or nice
    
    pass

@app.route('/login')
def login():

    #login screen will authenticate a user
    
    pass

@app.route('/logout')
def logout():

    #logout will end the user's session
    
    pass

@app.route('/view_players')
def view_players():

    #takes to a screen where all players are lists, and also indicates
    #if each player has cast their vote for each voting session yet
    #or not
    pass

@app.route('/my_role/<int:userid>')
def my_role(userid):

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

@app.route('/admin_screen')
def admin_screen():

    #only the admin can view this section.  allows amdin to contol the state of the game
    pass
    
