# <Game Name>

## Prerequisites

1. Python 3.6
2. pip
3. virtualenv
4. virtualenvwrapper

## To get started:

1. Clone the repository and cd into directory:
   `$ git clone https://github.com/dncswim76/xmas-game.git`

2. cd into directory:
   `$ cd xmas-game`

2. Create a virtual environment:
   `$ mkvirtualenv xmas-game`

3. Activate virtual environment:
   `$ workon xmas-game`

4. (Optional) Add the following to ~/.bashrc:
   ```
   $ export WORKON_HOME=~/Envs
   $ source /usr/local/bin/virtualenvwrapper.sh
   alias xmas-game="cd ~/xmas-game; workon xmas-game"
   ```

5. Install requirements:
   `$ pip install -r requirements/requirements.txt`

6. Configure Database:
   `$ python run.py db upgrade`

7. Run server
   `$ python run.py runserver`
