#!/usr/bin/env python

import handler

class Home(handler.Handler):
	def get(self):
		self.render("home.html")