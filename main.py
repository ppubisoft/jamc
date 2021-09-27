#!/usr/bin/env python3
from just_playback import Playback
from pydub import AudioSegment

import sys
import os
import time
import eyed3
import datetime
import curses

cachedir = os.environ['HOME'] + "/.cache/jamp/"

try:
    os.mkdir(cachedir)
except FileExistsError:
    pass

printattrs = True

cachefile = cachedir + "cachefile.mp3"

userfile = sys.argv[1]

_, extension = os.path.splitext(userfile)

if extension not in [".flac", ".mp3"]:
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

def die(n, message="Exiting jamc..."):
    curses.curs_set(1)
    print(message)
    exit(n)


def handle_keypress(c, playback):
    if c == ' ':
        playback.resume() if playback.paused else playback.pause()
    elif c == 'h' or c == "KEY_LEFT":
        playback.seek(playback.curr_pos - 5)
#    elif c == ord('j'):
#        playback.set_volume(playback.volume - 0.1)
#    elif c == ord('k'):
#        playback.set_volume(playback.volume + 0.1)
    elif c == 'l' or c == "KEY_RIGHT":
        playback.seek(playback.curr_pos + 5)
    elif c == 'q':
        die(0)

def main(stdscr, playback):
    # hide cursor
    curses.curs_set(0)
    # make getch() non-blocking
    stdscr.nodelay(True)
    # init colourscheme
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    global printattrs # i used global, so sue me
    if printattrs:
        stdscr.addstr(f"{tag.title} - {tag.artist}\n", curses.color_pair(1))
    while playback.curr_pos != playback.duration:
        stdscr.addstr(f"{datetime.timedelta(seconds=round(playback.curr_pos))}/{datetime.timedelta(seconds=round(playback.duration))}\r", curses.color_pair(1))
        try:
            c = stdscr.getkey()
        except curses.error:
            continue
        handle_keypress(c, playback)
        stdscr.refresh()
        time.sleep(0.1)

try:
    curses.wrapper(main, playback)
except KeyboardInterrupt:
    die(0)
