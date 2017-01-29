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
import re

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Sign Up Form</title>
    <style type="text/css">
        .error {
            color: red;
            font-size: 1.5rel;
            font-weight: bold;
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
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    valid = True
    if USER_RE.match(username) == None:
        valid = False
    return valid

def valid_email(email):
    USER_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    valid = True
    if USER_RE.match(email) == None:
        valid = False
    return valid

def valid_password(password):
    USER_RE = re.compile(r"^.{3,20}$")
    valid = True
    if USER_RE.match(password) == None:
        valid = False
    return valid


class MainHandler(webapp2.RequestHandler):

    def get(self):
        username = self.request.get("username")
        email = self.request.get("email")
        signup_form = """
            <form action="/" method="post">
                <label>Username <input type="text" name="username" value="%(username)s" /></label><br><br>
                <label>Password <input type="password" name="password" /></label><br><br>
                <label>Re-enter Password <input type="password" name="verify" /></label><br><br>
                <label>Email address (optional)<input type="text" name="email" value="%(email)s"/></label><br><br>
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
        email = self.request.get("email")
        email = cgi.escape(email)
        p1 = self.request.get("password")
        p2 = self.request.get("verify")
        err_message = ""
        if username == "":
            err_message = "Please enter a username<br>"
        else:
            if valid_username(username) == False:
                err_message = "Username Invalid. Please try again.<br>"
        if valid_password(p1) == False:
            err_message += "Please enter a valid password.<br>"
        else:
            if p1 != p2:
                err_message += "Passwords do not match.<br>"
        if email != "":
            if valid_email(email) == False:
                err_message += "Please enter a valid email address or leave blank.<br>"


        if err_message != "":
            self.redirect("/?error=" + err_message + "&username=" + username + "&email=" + email)
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
