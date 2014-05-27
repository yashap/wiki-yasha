#!/usr/bin/env python

import handler
import re
from entities import User

class Login(handler.Handler):
	def get(self):
		next_url = self.request.headers.get("referer", "/")
		self.render("login.html", next_url=next_url)

	def post(self):
		next_url = str(self.request.get("next_url"))
		if not next_url or re.match(r"(.*)/(login|signup|logout)/?", next_url):
			next_url = "/"

		username = self.request.get("username")
		password = self.request.get("password")

		u = User.User.login(username, password)
		# remember that User.login just checks the db to see if the username and pw are valid
		# 	if so, it returns the user object from the db
		# it doesn't actually set the user cookie

		if u:
			self.login(u)
			# that sets the cookie!
			self.redirect(next_url)
		else:
			self.render("login.html", next_url=next_url, error="Invalid login.")
