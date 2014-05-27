#!/usr/bin/env python

import handler

class Logout(handler.Handler):
	def get(self):
		self.logout()
		self.redirect(self.request.referer)
