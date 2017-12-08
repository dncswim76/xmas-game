from xmas_game import app, db, login_manager
from .models import Setting, User, Vote, Player
import random

#returns the game state
def get_game_state():
    return Setting.query.filter(Setting.config_var=='game_state').first().value

#updates the current round of the game
def get_game_round():
    return Setting.query.filter(Setting.config_var=='game_round').first().value

def get_percent_naughty():
    return Setting.query.filter(Setting.config_var=='percent_naughty').first().value


#updates the state to a new value
def set_game_state(new_state):
    state_setting = Setting.query.filter(Setting.config_var=='game_state').first()
    state_setting.value = new_state
    db.session.commit()


#gets the current round of the game
def set_game_round(new_round):
    round_setting = Setting.query.filter(Setting.config_var=='game_round').first()
    round_setting.value = new_round
    db.session.commit()

#kills the current game and creates a new one
def start_new_game():
    set_game_state('STATE_ENTER')
    set_game_round(str(1))
    Player.query.delete()
    Vote.query.delete()
    db.session.commit()
    return None

#assigns roles to all players, assigning only a certain percentage of
#people to the naughty team based on a game setting
def assign_roles():

    #get all players and determine the number of naughty players
    all_players = Player.query.all()
    num_players = len(all_players)
    percent_naughty = float(get_percent_naughty())/100
    num_naughty = int(num_players * percent_naughty)

    i = num_naughty
    while(i > 0):

        #choose a random person of the players
        random_person = all_players[random.randint(0, num_players-1)]
        #make sure the same person wasn't selected twice
        if (random_person.role != Player.Roles.NAUGHTY):
            random_person.role = Player.Roles.NAUGHTY
            db.session.commit()
            i = i - 1
            
    return

def cast_vote(voter_player_id, voted_for_player_id, vote_round):

    voter_player = Vote.query.filter(Vote.voting_round==vote_round and Vote.player==voter_player_id).first()

    #cast vote,  if didn't already vote
    if (voter_player is None):
        new_vote = Vote(player_id=voter_player_id, voting_round=vote_round, vote_id=voted_for_player_id)
        db.session.add(new_vote)
        db.session.commit()
    else:
        voter_player.vote=voted_for_player_id
        db.session.commit()

    #log that this player voted in this round
    player = Player.query.filter(Player.id==voter_player_id).first()
    if (vote_round == 1):
       player.voted_round_one="YES"
    if (vote_round == 2):
       player.voted_round_two="YES"
    if (vote_round == 3):
       player.voted_round_three="YES"
    if (vote_round == 4):
       player.voted_round_four="YES"
    db.session.commit()

    return


        

#returns an object to the player that won
def determine_round_winner(vote_round):

    #query for all votes in that round
    all_votes_round = Vote.query.filter(Vote.voting_round==vote_round)
    vote_ids = []

    #get player id of all votes, then find most occuring player
    for one_vote in all_votes_round:
        vote_ids.append(one_vote.vote_id)
    if (vote_ids != []):        
        winner = max(set(vote_ids), key=vote_ids.count)
        return Player.query.filter(Player.id==winner).first()
    else:
        return None
        
    


#advances the game state machine
def advance_the_game():

    current_state = get_game_state()
    current_round = int(get_game_round())
                   
    #after welcome stage, assign roles and let user's
    #view their role
    if (current_state == "STATE_ENTER"):
        assign_roles()
        set_game_state("STATE_VIEW_ROLE")
        return

    #once players have viewed their roles allow them to collaborate
    if (current_state == "STATE_VIEW_ROLE"):
        set_game_state("STATE_COLLABORATE")
        return

    #once voting is done, then tell users to vote via text
    #and then indicate to nominate
    if (current_state == "STATE_COLLABORATE"):
        set_game_state("STATE_VOTE")
        return

    #tallies up the votes for the round and then goes to the next round
    #or to the final vote
    if (current_state == "STATE_VOTE"):
                
        #nomination phase still not over, need to
        #continue to nominate more people
        if (current_round < 4):
            set_game_round(str(current_round+1))            
            set_game_state("STATE_COLLABORATE")
        else:            
            set_game_state("STATE_GAME_OVER")

        return
    
    if (current_state == "STATE_GAME_OVER"):
        start_new_game()
        set_game_state("STATE_ENTER")
        return

    return None
