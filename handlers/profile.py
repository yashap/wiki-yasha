#!/usr/bin/env python

import handler
import utils
import entities

class Profile(handler.Handler):
	def get(self):
		if not self.user:
			self.redirect("/signup")

		upd_pro = self.request.get("upd_pro")
		upd_pwd = self.request.get("upd_pwd")

		if upd_pro == "1":
			email = self.user.email if self.user.email else ""
			bio = self.user.bio if self.user.bio else ""
			self.render("update_profile.html", email=email, bio=bio)
		elif upd_pwd == "1":
			self.render("change_password.html")
		else:
			self.render("profile.html")

	def post(self):
		if not self.user:
			self.redirect("/signup")

		upd_pro = self.request.get("upd_pro")
		upd_pwd = self.request.get("upd_pwd")

		if upd_pro == "1":
			self.email = self.request.get("email") if self.request.get("email") else self.user.email
			self.bio = self.request.get("bio") if self.request.get("bio") else self.user.bio

			have_error = False
			params = {
				"email": self.email,
				"bio": self.bio
			}

			if not utils.valid_email(self.email):
				params["error"] = "That's not a email."
				have_error = True

			if have_error:
				self.render("update_profile.html", **params)
			else:
				u = self.user
				u.email = self.email
				u.bio = self.bio
				u.put()

				self.redirect("/profile")

		if upd_pwd == "1":
			self.password = self.request.get("password")
			self.new_pwd = self.request.get("new_pwd")
			self.verify = self.request.get("verify")

			have_error = False
			params = {"password": self.password,
				"new_pwd": self.new_pwd,
				"verify": self.verify
			}

			if not utils.valid_password(self.new_pwd):
				params["error"] = "That's not a valid password."
				have_error = True
			elif self.new_pwd != self.verify:
				params["error"] = "Your passwords don't match."
				have_error = True
			elif not entities.User.User.login(self.user.name, self.password):
				# Note that User.login takes a username and pw, and returns the user object if the pw is correct
				params["error"] = "That's not your current password."
				have_error = True

			if have_error:
				self.render("change_password.html", **params)
			else:
				u = self.user
				new_pw_hash = entities.User.make_pw_hash(self.user.name, self.new_pwd)
				print new_pw_hash
				u.pw_hash = new_pw_hash
				u.put()

				self.redirect("/profile")

