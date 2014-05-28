# !/usr/bin/env python

import os
import jinja2
import hmac
import re

from entities import Page
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
# if valid, return the regex match object

pass_regex = re.compile(r"^.{3,20}$")
def valid_password(password):
	return password and pass_regex.match(password)
# if valid, return the regex match object

email_regex = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
	return not email or email_regex.match(email)
# either need no email, or a valid email, to return the regex match object

page_id_regex = re.compile(r"^[a-zA-Z0-9_-]{2,30}$")
reserved_pages = ["signup", "logout", "login", "profile", "welcome", "newpage", "_edit"]
def valid_page_id(page_id):
	if page_id_regex.match(page_id) and page_id not in reserved_pages and js_index(page_id, " ") == -1:
		if Page.Page.by_page_id(page_id):
			return {"is_valid": False, "error": "That page name is already taken"}
		else:
			return {"is_valid": True}
	else:
		return {"is_valid": False, "error": "That is not a valid page name"}

# General utils
###############################
def js_index(data, element):
	try:
		return  data.index(element)
	except ValueError:
		return -1