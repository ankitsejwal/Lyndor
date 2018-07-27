#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' rename video and subtitle files '''

import os

def videos(path):
    ''' Rename videos '''
    print('\n🔰  Renaming video/subtitle files\n')
    for vid in os.listdir(path):
        if vid.endswith('.mp4'):
            # remove leading space in the end of the video file
            if vid[-5] == ' ':
                new_name = vid[:-5] + '.mp4'
                os.rename(os.path.join(path, vid), os.path.join(path, new_name))
                print('renamed >>> ' + new_name)


def subtitles(path):
    ''' Rename subtitles '''
    for sub in os.listdir(path):
        if sub.endswith('.en.srt'):
            # remove leading space with subtitle files
            if sub[-8] == ' ':
                new_name = sub[:-8] + '.en.srt'
                os.rename(os.path.join(path, sub), os.path.join(path, new_name))
                print('renamed >>> ' + new_name)