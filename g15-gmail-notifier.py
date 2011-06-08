#!/usr/bin/env python
# (c) 2008 Gurpartap Singh — http://gurpartap.com
"""Usage: g15-gmail-notifier [OPTIONS]

'G15 Gmail notifier' provides periodic updates that pertain to the user's gmail inbox. The notifier working in background, displays a message on the LCD of Logitech's G15 keyboard, when the user recieves new mail, and allows to open inbox directly from the G15 buttons.

Examples:
  g15-gmail-notifier -l eBay            # Check for e-mails labelled "eBay".
  g15-gmail-notifier -d 5               # Check for e-mails every 5 seconds.
  g15-gmail-notifier -u name -p pass    # Pass login credentials directly.

Option  GNU long version   Meaning
-u      --username         Gmail account name or e-mail address
-p      --password         Accompanying password
-l      --label            Folder label to browse e.g. all, spam, etc. [inbox]
-d      --delay            Time interval, in seconds, to check new mails. [10]"""

#  G15 Gmail notifier
#
#  g15-gmail-notifier is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  g15-gmail-notifier is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with g15-gmail-notifier; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#  (c) 2008 Gurpartap Singh — http://gurpartap.com

import sys, getopt
import sched, time
import subprocess
import webbrowser
from getpass import getpass

username = ""
password = ""
label = "inbox"
delay = int(10)

def main(username, password, label, delay):
  try:
    import libgmail
  except ImportError:
    print "\033[31m" + " [31mlibgmail is missing." + "\033[0;0m"
    return 1

  try:
    opts, args = getopt.getopt(sys.argv[1:], "hu:p:l:d:", ["help", "username=", "password=", "label=", "delay="])
  except getopt.error, msg:
    print "g15-gmail-notifier: %s" % msg
    print __doc__
    sys.exit(2)

  for o, a in opts:
    if o in ("-h", "--help"):
      print __doc__
      sys.exit(0)
    elif o in ("-u", "--username"):
      username = a
    elif o in ("-p", "--password"):
      password = a
    elif o in ("-l", "--label"):
      label = a
    elif o in ("-d", "--delay"):
      delay = int(a)

  if len(username) == 0:
    username = raw_input("Gmail account name: ")
  if len(password) == 0:
    password = getpass("Password: ")

  subprocess.call("clear")
  print "Attempting to login using username '%s'..." % username
  mail = libgmail.GmailAccount(username, password)

  try:
    mail.login()
  except libgmail.GmailLoginFailure:
    print "Login attempt failed!\nCheck your username or password and make sure you are connected to the internet."
    raise SystemExit(1)
  #except httplib.BadStatusLine:
  #  print "Please make sure you are connected to the internet."
  #  raise SystemExit(1)
  else:
   print "Login attempt successful."

  checkGmail(label, delay, mail)

def checkGmail(label, delay, mail, last_count = 0):
  count = 0
  timedelay = delay
  scheduler = sched.scheduler(time.time, time.sleep)

  print "Checking for unread e-mail(s) with label '%s'..." % label
  if mail.getUnreadMsgCount(label):
    folder = mail.getUnreadMessages(label)
    count = len(folder)
    subprocess.call(["g15message", "-d", "1", "-t", "Checking...", "for unread mail(s)..."])
    if count > 1:
      title = "%d unread e-mails!" % len(folder)
      goto = "Inbox" if label is "inbox" else "Gmail"
      msg = "Do you want to goto %s now?" % goto
      thread_id = ""
    else:
      title = "New e-mail received!"
      # The following will mark your message are "read".
      #msg = "%s: %s" % folder[0][0].sender, folder[0][0].subject
      msg = "Read the e-mail now?"
      thread_id = "/%s" % folder[0].id

    print "%d unread e-mail(s)!" % len(folder)
    if count > last_count:
      print "Awaiting user input..."
      if subprocess.call(["g15message", "-c", "-y", "-t", title, msg]):
        print "Launching Gmail..."
        default_labels = ["inbox", "starred", "chats", "sent", "drafts", "all", "spam", "trash"]
        url = label if label in default_labels else "label/%s" % label
        webbrowser.open_new_tab("http://mail.google.com/mail/#%s%s" % (url, thread_id))
        timedelay += 50
      else:
        print "Negative signal received. Notification for current unread e-mail(s) disabled."
    else:
      subprocess.call(["g15message", "-d", "3", "-c", "-t", "No /new/ e-mail(s).", "However, %s" % ("%d Unread Message(s)!" % len(folder))])
  else:
    print "No unread e-mail(s)"
  
  print "Checking for unread e-mail(s) in %d seconds..." % timedelay
  scheduler.enter(timedelay, 1, checkGmail, (label, delay, mail, count,))
  scheduler.run()

if __name__ == "__main__":
  sys.exit(main(username, password, label, delay))
