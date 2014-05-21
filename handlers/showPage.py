#!/usr/bin/env python

import handler
from entities import Page

class showPage(handler.Handler):
	def get(self, page_id):
		self.page_id = page_id[1:]

		q = Page.Page.by_page_id(self.page_id)
		if q:
			self.render("page.html", title=q.title, content=q.content, created=q.created, last_modified=q.last_modified)

		else:
			self.redirect("/_edit/%s" % self.page_id)

