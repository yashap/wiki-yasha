#!/usr/bin/env python

import handler
import utils
from entities import Page

class Home(handler.Handler):
	def get(self):
		top_pages = Page.Page.top_10()
		for i in range(len(top_pages)):
			content = top_pages[i].content
			cutoff = 300
			if content.count("\n") > 3:
				cutoff = utils.findnth(content, "\n", 3) - 1
				cutoff = cutoff if cutoff < 300 else 300
			top_pages[i].content = top_pages[i].content[:cutoff] + " ..."
		self.render("home.html", top_pages=top_pages)