#!/usr/bin/env python

import handler
import utils
from entities import Page

class EditPage(handler.Handler):
	def get(self, page_id):
		# in main.py, page_id is automatically passed to the handler
		if not self.user:
			self.redirect("/signup")

		q = Page.Page.by_page_id(page_id)
		self.created_user = q.created_user if q else None
		self.page_id = page_id

		if q:
			self.render("edit_page.html", title=q.title, content=q.content, created=q.created, last_modified=q.last_modified)

		else:
			self.render("edit_page.html", title="New Page")

	def post(self):
		self.title = self.request.get("title")
		self.content = self.request.get("content")
		self.modified_user = self.user.name
		if not self.created_user:
			self.created_user = self.user.name

		have_error = False
		params = {"title": self.title,
			"content": self.content,
			"created_user": self.created_user,
			"modified_user": self.modified_user
		}

		if not utils.valid_title(self.username):
			params["error"] = "That's not a valid title."
			have_error = True
		elif not self.conent:
			params["error"] = "You must enter content for the page."
			have_error = True

		if have_error:
			self.render("edit_page.html", **params)
		else:
			p = Page.Page(title=self.title, content=self.content, created_user=self.created_user, modified_user=self.modified_user)
			p.put()

			self.redirect("/" + self.page_id)
