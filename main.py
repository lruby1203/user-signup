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
        error_string = self.request.get("error")
        error_list = error_string.split()
        err_mess1 = ""
        err_mess2 = ""
        err_mess3 = ""
        err_mess4 = ""


#        index = 0
#        while error_string != "":

        if "blank" in error_list:
            err_mess1 = """<td><span class="error">Please enter a username.</span></td>"""
        if "user_invalid" in error_list:
            err_mess1 = """<td><span class="error">Please enter a valid username.</span></td>"""
        if "pass_invalid" in error_list:
            err_mess2 = """<td><span class="error">Please enter a valid password.</span></td>"""
        if "pass_blank" in error_list:
            err_mess2 = """<td><span class="error">Please enter a password.</span></td>"""
        if "match" in error_list:
            err_mess3 = """<td><span class="error">Passwords do not match. Please re-enter.</span></td>"""
        if "email_invalid" in error_list:
            err_mess4 = """<td><span class="error">Please enter a valid email or leave this field blank.</span></td>"""
        top_of_table = """<form action="/" method="post">
                <table>
                    <tr>
                        <td><label>Username </label></td>
                        <td><input type="text" name="username" value="%(username)s" /></td>"""
        row_2 = """</tr>

            <tr>
                <td><label>Password </label></td>
                <td><input type="password" name="password" /></td>
            """
        row_3 = """</tr><tr>
                <td><label>Re-enter Password </label></td>
                <td><input type="password" name="verify" /></td>
            """
        row_4 = """</tr><tr>
                <td><label>Email address (optional)</label></td>
                <td><input type="email" name="email" value="%(email)s"/></td>
            """
        close_table = """</tr></table>
            <input type="submit" name="submit" />
            </form>"""
        signup_form = top_of_table + err_mess1 + row_2 + err_mess2 + row_3 + err_mess3 + row_4 + err_mess4 + close_table







        content = page_header + signup_form % {"username": username, "email":email} + page_footer
        self.response.write(content)

    def post(self):
        username = self.request.get("username")
        username = cgi.escape(username)
        email = self.request.get("email")
        email = cgi.escape(email)
        p1 = self.request.get("password")
        p2 = self.request.get("verify")
        error = ""
        if username == "":
            error += "blank "
        else:
            if valid_username(username) == False:
                error += "user_invalid "
        if p1 == "":
            error += "pass_blank "
        else:
            if valid_password(p1) == False:
                error += "pass_invalid "
            else:
                if p1 != p2:
                    error += "match "
        if email != "":
            if valid_email(email) == False:
                error += "email_invalid"


        if error != "":
            self.redirect("/?error=" + error + "&username=" + username + "&email=" + email)
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
