#!/usr/bin/env python

import handler
from entities import Page

class EditPage(handler.Handler):
	def get(self, page_id):
		# in main.py, page_id is automatically passed to the handler
		q = Page.Page.by_page_id(page_id)
		if q:
			self.render("edit_page.html", title=q.title, content=q.content, created=q.created, last_modified=q.last_modified)

		else:
			self.render("edit_page.html", title="filler", content="filler", created="filler", last_modified="filler")
