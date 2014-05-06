#!/usr/bin/env python

import handler
from entities import User

class Login(handler.Handler):
	def get(self):
		self.render("login.html")

	def post(self):
		username = self.request.get("username")
		password = self.request.get("password")

		u = User.User.login(username, password)
		# remember that User.login just checks the db to see if the username and pw are valid
		# 	if so, it returns the user object from the db
		# it doesn't actually set the user cookie

		if u:
			self.login(u)
			# that sets the cookie!
			self.redirect("/welcome")
		else:
			self.render("login.html", error = "Invalid login.")
