# Scribbl+ by write_illegibly
Soojin Choi(PM), Emily Lee, Kevin Lin, Angela Tom
## Project Overview

## Necessary Packages

## Launch Instructions
### Run on localhost
1. Copy the ssh/https link found [here](https://github.com/Soojin-C/write_illegibly)
2. Clone the repo by running `$ git clone <link>`
3. Have the latest version of Python installed (Python 3.7.2)
4. Install virtualenv by running `$ pip3 install virtualenv`
   * Make a venv by running `$ python3 -m venv VENV_NAME`
   * Activate it by running `$ . ~/path_to_venv/VENV_NAME/bin/activate`
   * Deactivate it by running `$ deactivate`
5. Activate your virtual environment
6. In the root of the directory, move to the directory named scribble and run `$ pip install -r requirements.txt`
7. Now you are ready to run the flask app. Run the command `$ python __init__.py`. (Make sure your virtual enviornment is actvated)
8. Launch the app in your browser (http://127.0.0.1:5000/)

### Run on Apache2
1. Copy the https link under Clone and download
2. ssh into your droplet through a user using `$ ssh <user>@<ip address>`
3. Go to the directory /var/www through `$ cd /var/www/` 
4. Clone the repo and name the directory your chosen appname by running 
  `$ sudo git clone https://github.com/Soojin-C/write_illegibly.git scribble`
   * The tree of the directory should be:
      * scribble
         * scribble
         * scribble.wsgi
         * scribble.conf
5. Move the .conf file to the /etc/apache2/sites-available directory by running the command 
`$ sudo mv /var/www/scribble/scribble.conf /etc/apache2/sites-available`
   * Make sure that the ServerName in scribble.conf is set to your droplet ip.
   * Make sure there are no other .conf files with the same ip as the one you place into scribble.conf
   * Enable your site by running the command `$ sudo a2ensite scribble`
6. Go into the first directory named scribble and run both 
    1. `$ sudo chgrp -R www-data scribble`
    2. `$ sudo chmod -R g+w scribble`
7. Install virtualenv by running `$ pip3 install virtualenv`
   * Make a venv by running `$ python3 -m venv VENV_NAME`
   * Activate it by running `$ . ~/path_to_venv/VENV_NAME/bin/activate`
   * Deactivate it by running `$ deactivate`
8. Activate your virtual environment 
9. Go into the second directory named scribble and run `$ pip install -r requirements.txt`
10. After running everything above, run `$ sudo service apache2 restart`
   * Run this anytime you make changes as well
11. Go to your ip address to view your app
12. If there are any problems, check the error log by running `$ sudo cat /var/log/apache2/error.log`
