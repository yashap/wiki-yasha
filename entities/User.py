# !/usr/bin/env python

import random
import string
import hashlib

from google.appengine.ext import db

def make_salt():
	return "".join(random.choice(string.ascii_letters) for x in range(5))

def make_pw_hash(name, pw, salt=None):
	if not salt:
		salt = make_salt()
	h = hashlib.sha256(name + pw + salt).hexdigest()
	return "%s|%s" % (salt, h)

def valid_pw(name, pw, h):
	salt = h.split("|")[0]
	return h == make_pw_hash(name, pw, salt)

def user_key():
	return db.Key.from_path("Wiki_user_kind", "Wiki_user_name")
	# When creating User entities, I can set parent = user_key()
	# This will set the parent to a semi-fictional Datastore entity, with:
	# 	kind "Wiki_user_kind"
	# 	name "Wiki_user_name"
	# This will really just force strong consistency with any queries related to users

class User(db.Model):
	name = db.StringProperty(required = True)
	pw_hash = db.StringProperty(required = True)
	email = db.StringProperty()
	bio = db.StringProperty()
	created = db.DateTimeProperty(auto_now_add = True)
	last_modified = db.DateTimeProperty(auto_now = True)

	@classmethod
	def by_id(cls, uid):
		return cls.get_by_id(uid, parent = user_key())

	@classmethod
	def by_name(cls, name):
		return cls.all().filter("name =", name).ancestor(user_key()).get()
		# u = db.GqlQuery("SELECT * FROM User WHERE name = :1", name).get()
		# return u

	@classmethod
	def register(cls, name, pw, email=None, bio=None):
		pw_hash = make_pw_hash(name, pw)
		return User(
			parent = user_key(),
			name = name,
			pw_hash = pw_hash,
			email = email,
			bio = bio
		)

	@classmethod
	def login(cls, name, pw):
		u = cls.by_name(name)
		if u and valid_pw(name, pw, u.pw_hash):
			return u
