#!/usr/bin/python
import sys
sys.path.insert(0,"/var/www/scribble/")
sys.path.insert(0,"/var/www/scribble/scribble/")

import logging
logging.basicConfig(stream=sys.stderr)

from scribble import app as application
