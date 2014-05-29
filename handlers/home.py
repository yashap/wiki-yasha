#!/usr/bin/env python

import handler
import utils
from entities import Page

class Home(handler.Handler):
	def get(self):
		top_pages = Page.Page.top_10()
		for i in range(len(top_pages)):
			max_chars = 300
			max_lines = 3
			content = top_pages[i].content
			line_count = content.count("\n")
			if len(content) > max_chars or line_count > max_lines:
				pos = utils.findnth(content, "\n", max_lines) - 1
				cutoff = min(pos, max_chars) if pos > 5 else max_chars
				print("pos: %s; max_chars: %s; cutoff: %s" % (pos, max_chars, cutoff))
				top_pages[i].content = content[:cutoff] + " ..."
		self.render("home.html", top_pages=top_pages)