#!/usr/bin/env python

import handler
from entities import Page

class Home(handler.Handler):
	def get(self):
		top_pages = Page.Page.top_10()
		self.render("home.html", top_pages=top_pages)