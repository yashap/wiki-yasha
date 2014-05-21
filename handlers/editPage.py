#!/usr/bin/env python

import handler
from entities import Page

class EditPage(handler.Handler):
	def get(self, page_id):
		# in main.py, page_id is automatically passed to the handler
		if not self.user:
			self.redirect("/signup")

		page_id = page_id[1:]
		q = Page.Page.by_page_id(page_id)

		if q:
			self.render("edit_page.html", title=q.title, content=q.content, created=q.created, last_modified=q.last_modified)

		else:
			self.render("edit_page.html", title="New Page")

	def post(self, page_id):
		q = Page.Page.by_page_id(page_id)

		if q:
			self.created_user = q.created_user
			self.title = self.request.get("title") if self.request.get("title") else q.title
			self.content = self.request.get("content") if self.request.get("content") else q.content
		else:
			self.created_user = self.user.name
			self.title = self.request.get("title")
			self.content = self.request.get("content")

		self.modified_user = self.user.name
		self.page_id = page_id[1:]

		have_error = False
		params = {"title": self.title,
			"content": self.content,
			"created_user": self.created_user,
			"modified_user": self.modified_user,
			"page_id": self.page_id
		}

		if not self.title:
			params["error"] = "You must enter a title."
			have_error = True
		elif not q and Page.Page.by_title(self.title):
			params["error"] = "That title is already taken."
			have_error = True
		elif not self.content:
			params["error"] = "You must enter content for the page."
			have_error = True

		if have_error:
			self.render("edit_page.html", **params)
		else:
			p = Page.Page(title=self.title, content=self.content, created_user=self.created_user, modified_user=self.modified_user, page_id=self.page_id)
			p.put()

			self.redirect("/%s" % self.page_id)
