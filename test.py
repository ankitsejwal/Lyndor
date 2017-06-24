import urllib2
import re
import install
import os, sys
import run
import time
import datetime
import message
import draw
import threading

#!/usr/bin/env python
# taken from: http://stackoverflow.com/questions/7039114/waiting-animation-in-command-prompt-python

# class CursorAnimation(threading.Thread):
#     def __init__(self):
#         self.flag = True
#         self.animation_char = "|/-\\"
#         self.idx = 0
#         threading.Thread.__init__(self)

#     def run(self):
#         while self.flag:
#             print "Processing... ",
#             print self.animation_char[self.idx % len(self.animation_char)] + "\r",
#             self.idx += 1
#             time.sleep(0.1)

#     def stop(self):
#         self.flag = False

# if __name__ == '__main__':
#     spin = CursorAnimation()

#     # Start Animation
#     spin.start()

#     # Do something here
#     # Example: sleep
#     time.sleep(5)

#     # Stop Animation
#     spin.stop()
# Spinning cursor

animals = ['dog', 'cat', 'mouse', 'elephant', 'giraffe']

for animal in animals:
    if animal == 'mouse':
        print 'found mouse at position:' + animal