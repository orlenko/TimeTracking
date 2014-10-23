#!/usr/bin/python

import os
import os.path
import time
import datetime
import subprocess


HERE = os.path.dirname(os.path.abspath(__file__))
TICK_MINOR = os.path.join(HERE, 'coin.wav')
TICK_MAJOR = os.path.join(HERE, 'pouch.mp3')
PERIOD_MIN = 15



def play(filepath):
    print 'Playing file: %s' % filepath
    if not os.path.exists(filepath):
        print 'Oops, %s does not exist!' % filepath
        return 
    subprocess.call(['avplay', '-nodisp', '-autoexit', filepath])


def main():
    play(TICK_MAJOR)
    time.sleep(1)
    play(TICK_MINOR)
    while 1:
        print '.',
        now = datetime.datetime.now()
	minute = now.minute
	if minute:
            if minute % PERIOD_MIN == 0:
                play(TICK_MINOR)
                time.sleep(58.9)
        else:
            play(TICK_MAJOR)
            time.sleep(58.9)
        time.sleep(10)


if __name__ == '__main__':
    main()

