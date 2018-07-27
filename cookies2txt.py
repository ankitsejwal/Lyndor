#!/usr/bin/env python3
##########
# A simple tool to extract particular cookies from firefox's cookies.sqlite
# file and dump them to a legacy Netscape cookies.txt file.
##########
# ver	YYYY-MM-DD comment
# 0.9	2018-04-15 public release
#
##########
import sqlite3 as sql
from pathlib import Path


# Open the cookies database
db = sql.connect("/Users/ebarrab/Desktop/lyndor/cookies.sqlite")

# Fetch anything that might be of value to me.
# In this case crunchyroll, vrv, and cloudflare
### TODO: generate this from a short array of sites/paterns
## `host`,`?isGlobal?`,`path`,`isSecure`,`expiry`,`name`,`value`
resp = db.execute(	"SELECT `host`,`path`,`isSecure`,`expiry`,`name`,`value` "+
					"FROM `moz_cookies` WHERE "+
					"`host` LIKE '%crunchyroll%' OR "+
					"`host` LIKE '%vrv%' OR "+
					"`host` LIKE '%cloudflare%' "+
					"ORDER BY `host` ASC")
cookies = resp.fetchall();

def trueFalseStr(myBool):
	if (myBool == 0 or myBool == False):
		return('FALSE')
	else:
		return('TRUE')

# Now open the output file location and write the standard header
outputFile = "cookies.txt"
fh = open(outputFile, 'w')
fh.write(	"# Netscape HTTP Cookie File\n"+
			"# http://curl.haxx.se/rfc/cookie_spec.html\n"+
			"# This is a generated file!  Do not edit.\n"+
			"\n")
# Now generate a line for each cookie
for cookie in cookies:
	# if a cookie starts with a period, it applies to all subdomain (I think)
	globalCookie = (cookie[0][0] == '.')
	
	cookie_list = list(cookie);
	cookie_list.insert(1, trueFalseStr(globalCookie))
	# Convert the ambigious storage format of flags to a string
	cookie_list[3]=trueFalseStr(cookie_list[3])
	cookie_list[4]=str(cookie_list[4])
	fh.write("\t".join(cookie_list) + "\n")
# And we're done!
fh.close()