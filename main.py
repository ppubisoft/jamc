#!/usr/bin/env python3
from just_playback import Playback
from pydub import AudioSegment

import sys
import os
import time
import eyed3
import datetime

cachedir = os.environ['HOME'] + "/.cache/jamp/"

try:
    os.mkdir(cachedir)
except FileExistsError:
    pass

printattrs = True

cachefile = cachedir + "cachefile.mp3"

userfile = sys.argv[1]

_, extension = os.path.splitext(userfile)

if extension not in [".mp3", ".flac"]:
    basefile = AudioSegment.from_file(userfile)
    basefile.export(cachefile, format="mp3")
else:
    cachefile = userfile

try:
    tag = eyed3.load(cachefile).tag
except AttributeError:
    print("Could not get file attributes. Probably isn't an mp3.")
    printattrs = False

playback = Playback(cachefile)
playback.play()

if printattrs:
    print(f"{tag.title} - {tag.artist}")

while playback.curr_pos != playback.duration:
    sys.stdout.write(f"{datetime.timedelta(seconds=round(playback.curr_pos))}/{datetime.timedelta(seconds=round(playback.duration))}\r")
    sys.stdout.flush()
    time.sleep(1)
