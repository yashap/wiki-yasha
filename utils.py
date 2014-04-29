# !/usr/bin/env python

import os
import jinja2
import hmac
import random
import string
import hashlib
import re

from google.appengine.ext import db

# Template boilerplate
###############################
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
	autoescape = True)

# Hashing functions for cookies
###############################
SECRET = "imsosecret"

def hash_str(s):
	return hmac.new(SECRET, s).hexdigest()
	# used for secure cookies, in make_secure_val

def make_secure_val(s):
	return "%s|%s" % (s, hash_str(s))
	# make_secure_val("12356")
	# 	"12356|8d8e8018be02969246ef4ac04bf2a151"

def check_secure_val(h):
	val = h.split("|")[0]
	if h == make_secure_val(val):
		return val
	# returns "val" if it's the right hash in "val|hash"

# Hashing functions for database
###############################

def blog_key(name = "default"):
	return db.Key.from_path("blogs", name)
	# As above, but it's an ancestor element, in the db, to store all our blog posts

# Form validation
###############################
user_regex = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
	return username and user_regex.match(username)

pass_regex = re.compile(r"^.{3,20}$")
def valid_password(password):
	return password and pass_regex.match(password)

email_regex = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
	return not email or email_regex.match(email)
