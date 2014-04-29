#!/usr/bin/env python

import webapp2
import json

import utils
from entities import User

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = utils.jinja_env.get_template(template)
		params["user"] = self.user
		return t.render(params)

	def render(self, template, **params):
		self.write(self.render_str(template, **params))

	def render_json(self, d):
		json_txt = json.dumps(d)
		self.response.headers["Content-Type"] = "application/json; charset=UTF-8"
		self.write(json_txt)

	def set_secure_cookie(self, name, val):
		cookie_val = utils.make_secure_val(val)
		self.response.headers.add_header(
			"Set-Cookie",
			"%s=%s; Path=/" % (name, cookie_val)
		)
		# After we verify a login attempt, we can pass the user id to this as val

	def read_secure_cookie(self, name):
		cookie_val = self.request.cookies.get(name)
		return cookie_val and utils.check_secure_val(cookie_val)
		# so if the cookie is legit (properly hashed):
		# 	this will return the user id since check_secure_val() takes in userid|hash

	def login(self, user):
		self.set_secure_cookie("user", str(user.key().id()))
		# to get the user id, we pass in the user object, then grab it with user.key().id()

	def logout(self):
		self.response.headers.add_header(
			"Set-Cookie",
			"user=; Path=/"
		)

	def initialize(self, *a, **kw):
		webapp2.RequestHandler.initialize(self, *a, **kw)
		uid = self.read_secure_cookie("user")
		self.user = uid and User.User.by_id(int(uid))
		# If the user is logged in (has secure cookie), then store user object in self.user

		if self.request.url.endswith(".json"):
			self.format = "json"
		else:
			self.format = "html"
