### Description

'G15 Gmail notifier' provides periodic updates that pertain to the user's gmail inbox. The notifier working in background, displays a message on the LCD of Logitech's G15 keyboard, when the user recieves new mail, and allows to open inbox directly from the G15 buttons.

### Usage

g15-gmail-notifier [[OPTIONS]]

### Requirements

- libgmail
- g15message

### Examples

    g15-gmail-notifier -l eBay            # Check for e-mails labelled "eBay".
    g15-gmail-notifier -d 5               # Check for e-mails every 5 seconds.
    g15-gmail-notifier -u name -p pass    # Pass login credentials directly.

### Options

    Option  GNU long version   Meaning
    -u      --username         Gmail account name or e-mail address
    -p      --password         Accompanying password
    -l      --label            Folder label to browse e.g. all, spam, etc. [inbox]
    -d      --delay            Time interval, in seconds, to check new mails. [10]

### License

g15-gmail-notifier is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

g15-gmail-notifier is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with g15-gmail-notifier; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

(c) 2008 Gurpartap Singh — http://gurpartap.com