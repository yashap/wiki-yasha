#!/usr/bin/env python

import handler
from entities import Page

class EditPage(handler.Handler):
	def get(self, page_id):
		if not self.user:
			self.redirect("/signup")

		self.page_id = page_id[1:]
		q = Page.Page.by_page_id(self.page_id)

		if q:
			self.render("edit_page.html", editing=True, title=q.title, content=q.content, created=q.created,
				last_modified=q.last_modified, created_user=q.created_user, modified_user=q.modified_user)

		else:
			self.render("edit_page.html", editing=False)

	def post(self, page_id):
		self.page_id = page_id[1:]

		q = Page.Page.by_page_id(self.page_id)


		self.created_user = q.created_user if q else self.user.name

		self.title = self.request.get("title")
		self.content = self.request.get("content")
		self.modified_user = self.user.name

		have_error = False
		params = {"title": self.title,
			"content": self.content,
			"created_user": self.created_user,
			"modified_user": self.modified_user,
			"page_id": self.page_id
		}

		if self.title:
			check_title = Page.Page.by_title(self.title).title if Page.Page.by_title(self.title) else None

		print self.title
		if not self.title:
			params["error"] = "You must enter a title."
			have_error = True
		elif (not q and check_title) or (q and check_title and q.title != self.title):
			params["error"] = "That title is already taken."
			have_error = True
		elif not self.content:
			params["error"] = "You must enter content for the page."
			have_error = True

		if have_error:
			self.render("edit_page.html", **params)
		else:
			if q:
				q.title=self.title
				q.content=self.content
				q.modified_user=self.modified_user
			else:
				q = Page.Page(title=self.title, content=self.content, created_user=self.created_user,
					modified_user=self.modified_user, page_id=self.page_id, parent=Page.page_key())
			q.put()

			self.redirect("/%s" % self.page_id)
