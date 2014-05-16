#!/usr/bin/env python

import handler
# from entities import Page

class NewPage(handler.Handler):
	def get(self):
		# Pass wrong responses
		self.render("new_page.html")

	def post(self):
		self.url = self.request.get("pagename")
		# Test if the page name is taken, if so throw error, else redirect
		self.redirect("/" + self.url)
