#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2

PAGE_RE = r"(/(?:[a-zA-Z0-9_-]+/?)*)"
app = webapp2.WSGIApplication(
	[
		(r"/", "handlers.home.Home"),
		(r"/signup/?", "handlers.signup.Signup"),
		(r"/logout/?", "handlers.logout.Logout"),
		(r"/login/?", "handlers.login.Login"),
		(r"/profile/?", "handlers.profile.Profile"),
		(r"/welcome/?", "handlers.welcome.Welcome"),
		(r"/newpage/?", "handlers.newPage.NewPage"),
		(r"/_edit" + PAGE_RE, "handlers.editPage.EditPage"),
		(PAGE_RE, "handlers.showPage.showPage")
	],
	debug=True
)
