import urllib2
import re
import install
import os

chapter_no = 0
chapter = '2. Layout, ASP.NET, Node, and Refactoring'

if chapter[1] == '.':
    chapter_name = chapter[3:]
    chapter = str(chapter_no) + '. ' + chapter_name
    chapter_no += 1
    print chapter
elif chapter[2] == '.':
    chapter_name = chapter[3:]
    chapter = str(chapter_no) + '. ' + chapter_name
    chapter_no += 1
    print chapter
else:
    chapter = str(chapter_no) + '. ' + chapter
    chapter_no += 1
    print chapter
