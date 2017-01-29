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
import cgi

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

def valid_username(username):
    illegal_chars = ()
    valid = True
    if len(username) < 3 or len(username) > 20:
        valid = False
    return valid

#def build_form(self, username="", email=""):
#    signup_form = """
#        <form action="/" method="post">
#            <label>Username <input type="text" name="username" value="%(username)s" /></label><br><br>
#            <label>Password <input type="password" name="password" /></label><br><br>
#            <label>Re-enter Password <input type="password" name="verify" /></label><br><br>
#            <input type="submit" name="submit" />
#        </form>
#        """
#    return signup_form

class MainHandler(webapp2.RequestHandler):

    def get(self):
        username = self.request.get("username")
        email = self.request.get("email")
        signup_form = """
            <form action="/" method="post">
                <label>Username <input type="text" name="username" value="%(username)s" /></label><br><br>
                <label>Password <input type="password" name="password" /></label><br><br>
                <label>Re-enter Password <input type="password" name="verify" /></label><br><br>
                <label>Email address (optional)<input type="Email" name="email" value="%(email)s"/></label><br><br>
                <input type="submit" name="submit" />
            </form>


            """
        content = page_header + signup_form % {"username": username, "email":email} + page_footer
        error = self.request.get("error")
        error_element = "<p class='error'>" + error + "</p>" if error else ""
        content += error_element
        self.response.write(content)

    def post(self):
        username = self.request.get("username")
        username = cgi.escape(username)
        err_message = ""
        if username == "":
            err_message = "Please enter a username"
        else:
            if valid_username(username) == False:
                err_message = "Username Invalid. Please try again."

        if err_message != "":
            self.redirect("/?error=" + err_message + "&username=" + username)
        else:
            self.redirect("/success?username=" + username)
class Success(webapp2.RequestHandler):
    def get(self, username=""):
        username = self.request.get("username")
        welcome_message = "<h2>Welcome, " + username + "</h2>"
        content = page_header + welcome_message + page_footer
        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/success', Success)
], debug=True)
