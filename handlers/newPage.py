#!/usr/bin/env python

import handler
import utils

class NewPage(handler.Handler):
	def get(self):
		if not self.user:
			self.redirect("/signup")

		# Pass wrong responses
		self.render("new_page.html")

	def post(self):
		self.page_id = self.request.get("page_id")
		self.valid_page = utils.valid_page_id(self.page_id)
		if self.valid_page["is_valid"]:
			self.redirect("/" + self.page_id)
		else:
			self.render("new_page.html", error=self.valid_page["error"])
