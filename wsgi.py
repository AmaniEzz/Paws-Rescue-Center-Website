#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/FlaskApp/")

import app as application
application.secret_key = 'HSHDBANYS6DJ2'
