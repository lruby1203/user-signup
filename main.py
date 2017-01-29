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
#
import webapp2

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Sign Up Form</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>
        <h1>User Sign Up</h1>
    </h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""
def build_form(self):
    signup_form = """
        <form action="/signup" method="post">
            <label>Username <input type="text" name="username" /></label><br><br>
            <label>Password <input type="password" name="password" /></label><br><br>
            <label>Re-enter Password <input type="password" name="verify" /></label><br><br>
            <label>Email address (optional)<input type="Email" name="email" /></label><br><br>
            <input type="submit" name="submit" />
        </form>


        """
    return signup_form

class MainHandler(webapp2.RequestHandler):

    def get(self):
        content = page_header + build_form(self) + page_footer
        self.response.write(content)

class SignUp(webapp2.RequestHandler):

    def post(self):
        username = self.request.get("username")
        welcome_message = "<h2>Welcome, " + username + "</h2>"
        content = page_header + welcome_message + page_footer
        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/signup', SignUp)
], debug=True)
