#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
import os
import urllib2
import json

cursor = "-1"
baseurl = "https://api.twitter.com/1/friends.json?screen_name=pzelnip"

users = []
while cursor != "0":
    url = baseurl + "&cursor=" + cursor

    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    data = json.loads(response.read())

    for i, item in enumerate(data['users']):
        users.append("@" + item['screen_name'])
    cursor = data['next_cursor_str']

users = " ".join(users)
os.system('ttytter.pl -verify -readline="%s"' % users)
