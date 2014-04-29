#!/usr/bin/env python

import handler

class Welcome(handler.Handler):
	def get(self):
		if self.user:
			self.render("welcome.html")
		else:
			self.redirect("/signup")
