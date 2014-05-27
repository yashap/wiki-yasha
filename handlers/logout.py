#!/usr/bin/env python

import handler
import re

class Logout(handler.Handler):
	def get(self):
		next_url = self.request.headers.get("referer", "/")
		if not next_url or re.match(r"(.*)/(login|signup|logout)/?", next_url):
			next_url = "/"

		self.logout()

		self.redirect(next_url)