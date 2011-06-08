#!/usr/bin/env python
# (c) 2008 Gurpartap Singh — http://gurpartap

import subprocess
import webbrowser

username = "you@gmail.com"
password = "lolphp"

try:
  import libgmail
except ImportError:
  print "libgmail is missing."
  raise SystemExit(1)

mail = libgmail.GmailAccount(username, password)

print "Logging in using username %s..." % username

try:
  mail.login()
except libgmail.GmailLoginFailure:
  print "Login failed!\nCheck your username or password and make sure you are connected to the internet."
  raise SystemExit(1)
else:
  print "Logged in successfully."

if mail.getUnreadMsgCount("inbox"):
  folder = mail.getUnreadMessages("inbox")
  if len(folder) > 1:
    title = "%d Unread Messages!" % len(folder)
    msg = "Do you want to goto Inbox now?"
    thread_id = ""
  else:
    title = "New e-mail received!"
    # The following will mark your message are "read".
    #msg = "%s: %s" % folder[0][0].sender, folder[0][0].subject
    msg = "Read the message now?"
    thread_id = "/" + folder[0].id

  if subprocess.call(["g15message", "-c", "-y", "-t", title, msg]):
    webbrowser.open_new_tab("http://mail.google.com/mail/#inbox%s" % thread_id)
