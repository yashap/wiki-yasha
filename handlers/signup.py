#!/usr/bin/env python

import handler
import utils
import entities
import re

class Signup(handler.Handler):
	def get(self):
		next_url = self.request.headers.get("referer", "/")
		self.render("signup.html", next_url=next_url)

	def post(self):
		have_error = False

		next_url = str(self.request.get("next_url"))
		if not next_url or re.match(r"(.*)/(login|signup)/?", next_url):
			next_url = "/"

		self.username = self.request.get("username")
		self.password = self.request.get("password")
		self.verify = self.request.get("verify")
		self.email = self.request.get("email")
		self.bio = None

		params = {"username": self.username,
			"password": self.password,
			"verify": self.verify,
			"email": self.email,
			"next_url": next_url
		}

		if not utils.valid_username(self.username):
			params["error"] = "That's not a valid username."
			have_error = True
		elif not utils.valid_password(self.password):
			params["error"] = "That's not a valid password."
			have_error = True
		elif self.password != self.verify:
			params["error"] = "Your passwords don't match."
			have_error = True
		elif not utils.valid_email(self.email):
			params["error"] = "That's not a email."
			have_error = True
		elif entities.User.User.by_name(self.username):
			params["error"] = "That username has already been taken."
			have_error = True

		if have_error:
			self.render("signup.html", **params)
		else:
			u = entities.User.User.register(self.username, self.password, self.email, self.bio)
			u.put()

			self.login(u)
			self.redirect(next_url)
