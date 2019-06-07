#!/usr/bin/python3
import sys
sys.path.insert(0,"/var/www/scribble/")
sys.path.insert(0,"/var/www/scribble/scribble/")

import logging
logging.basicConfig(stream=sys.stderr)

from <appname> import app as application
