

create table users (
  id integer primary key autoincrement,
  username text not null,
  password text not null,
  first_name text not null,
  last_name text not null,
  is_admin integer,
  phone_number text not null
);  
  

create table players (
  id integer,
  player_first_name text not null,
  player_last_name text not null,
  player_role       integer,
  player_vote1      integer,
  player_won_vote1  integer, 
  player_vote2      integer,
  player_won_vote2  integer, 
  player_vote3      integer,
  player_won_vote3  integer, 
  player_final_vote integer, 
  player_won_final  integer 
);

create table game_state(
  gstate integer,
  round integer
);  
