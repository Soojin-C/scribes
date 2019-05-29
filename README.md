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
6. In the root of the directory, run `$ pip install -r requirements.txt`
7. Now you are ready to run the flask app. Run the command `$ python app.py`. (Make sure your virtual enviornment is actvated)
8. Launch the app in your browser (http://127.0.0.1:5000/)

### Run on Apache2
1. Copy the https link under Clone and download
2. ssh into your droplet through a user using `$ ssh <user>@<ip address>`
3. Go to the directory www through `$ cd /var/www/` 
4. Clone the repo and name the directory your chosen appname by running `$ git clone <link> <appname>`
  * The tree of the directory should be:
      * appname
         * appname
         * appname.wsgi
  * Make sure you also have a <appname>.conf file with the path `/etc/apache2/sites-enabled/<appname>.conf`
  * Enable your site by running the command `$ sudo a2ensite <appname>`
5. Install virtualenv by running `$ pip3 install virtualenv`
   * Make a venv by running `$ python3 -m venv VENV_NAME`
   * Activate it by running `$ . ~/path_to_venv/VENV_NAME/bin/activate`
   * Deactivate it by running `$ deactivate`
6. Activate your virtual environment 
7. Go into the second directory named <appname> and run `$ pip install -r requirements.txt`
8. After running everything above, run `$ sudo service apache2 restart`
  * Run this anytime you make changes as well
9. Go to your ip address to view your app
10. If there are any problems, check the error log by running `$ sudo cat /var/log/apache2/error.log`

`$ sudo chgrp -R www-data <appname>`
`$ sudo chmod -R g+w <appname>`
