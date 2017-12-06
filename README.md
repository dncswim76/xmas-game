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


## To deploy on apache2:

1. Install Appache:
`$ apt-get install apache2`
`$ apt-get install libapache2-mod-wsgi`


2. Create file conf file in:
`/etc/apache2/sites-available/xmas_game.conf'

3. Put this in the file:

```
<VirtualHost *>
    ServerName xmas_game

    WSGIDaemonProcess xmas_game user=www-data group=www-data threads=5 home=/var/www/xmas_game/xmas-game
    WSGIScriptAlias / /var/www/xmas_game/xmas-game/xmas_game.wsgi
    
    <Directory /var/www/xmas_game/xmas-game>
            WSGIProcessGroup xmas_game
            WSGIApplicationGroup %{GLOBAL}
	    WSGIScriptReloading On	    
            Order deny,allow
            Allow from all
    </Directory>
    
</VirtualHost>
```

4. Make directory : `/www/var/xmas_game/`

5. In `/www/var/xmas_game`, clone git repository. Path shown in #3 to WSGI file should match.

6. In `config.py` make sure absolute path of data base is commented out.

7. If directory not already created, create the directory:
   `$ python run.py db upgrade`

8. Change user permissions on directory in `/www/var/xmas_game/xmas-game`

```
$sudo chown www-data. .
$sudo chown www-data. xmas_game.db
```

9. Enable new apache virtual host:
   `sudo a2ensite xmas_game`

10. NOTE: if you are running another virtual host in apache, you must disable it or round WSGIScriptAlias away from root of URL.
   (You can find the enabled sites in `/etc/apache2/sites-enabled`)
  `$ sudo a2dissite <enabled site>`
  
11. Restart apache server:
  `$ sudo /etc/init.d/apache2 restart`