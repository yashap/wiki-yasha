# !/usr/bin/env python

from google.appengine.ext import db

def page_key():
	return db.Key.from_path("Wiki_page_kind", "Wiki_page_name")

class Page(db.Model):
	page_id = db.StringProperty(required = True)
	title = db.StringProperty(required = True)
	content = db.StringProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	last_modified = db.DateTimeProperty(auto_now = True)
	created_user = db.StringProperty(required = True)
	modified_user = db.StringProperty(required = True)

	@classmethod
	def by_page_id(cls, page_id):
		# return cls.all().filter("page_id =", page_id).ancestor(page_key()).get()
		return cls.all().filter("page_id =", page_id).get()

	@classmethod
	def by_title(cls, title):
		return cls.all().filter("title =", title).ancestor(page_key()).get()
