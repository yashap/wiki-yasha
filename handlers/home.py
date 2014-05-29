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
			line_count = content.count("\n")
			max_lines = 3
			if len(content) > cutoff or line_count > max_lines:
				pos = utils.findnth(content, "\n", max_lines) - 1
				cutoff = min(pos, cutoff)
				top_pages[i].content = content[:cutoff] + " ..."
		self.render("home.html", top_pages=top_pages)