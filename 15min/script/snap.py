#!/usr/bin/python

import os
import time
import gtk.gdk


SNAPSHOT_DIR = '/home/vlad/capture/'
PAUSE_SEC = 60

FACTOR = .6


def check_duplicates(dirname):
    '''Find two most recent files in the directory. 
    If the files are identical, remove the latest one,
    and suffix the original with "xN", where N is the number
    of repeats.
    '''
    dirname = dirname or os.getcwd()
    filelist = []
    for fn in os.listdir(dirname):
        fname = os.path.join(dirname, fn)
        stat = os.stat(fname)
        filelist.append((fname, stat.st_mtime))
    if len(filelist) < 2:
        return
    filelist = sorted(filelist, key=lambda x: x[1])
    f1 = filelist[-2][0]
    f2 = filelist[-1][0]
    print 'Two newest files: %s and %s' % (f1, f2)
    data1 = open(f1, 'rb').read()
    data2 = open(f2, 'rb').read()
    if data1 == data2:
        # Files are identical
        print 'Same'
        count = 1
        noext = os.path.splitext(f1)[0]
        namebase = noext
        if 'x' in noext:
            parts = noext.split('x')
            namebase = parts[0]
            count = int(parts[1])
        newname = '%sx%s' % (namebase, count + 1)
        os.rename(f1, newname)
        os.unlink(f2)
    else:
        print 'Not the same'


def save_screen(filename):
    w = gtk.gdk.get_default_root_window() #@UndefinedVariable
    sz = w.get_size()
    pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, sz[0], sz[1]) #@UndefinedVariable
    pb = pb.get_from_drawable(w, w.get_colormap(), 0, 0, 0, 0, sz[0], sz[1])
    pb = pb.scale_simple(int(sz[0] * FACTOR), int(sz[1] * FACTOR), gtk.gdk.INTERP_BILINEAR) #@UndefinedVariable
    if pb:
        pb.save(filename, 'jpeg', {'quality': '30'})
        #check_duplicates(os.path.dirname(filename))
    else:
        print 'Unable to get the screenshot.'
    os.system('add-overlay %s %s' % (filename, os.path.basename(filename)))


def save_current():
    local = time.localtime()
    filename = ('screen-%04d-%02d-%02d-%02d-%02d-%03d.jpeg' %
                (local.tm_year,
                 local.tm_mon,
                 local.tm_mday,
                 local.tm_hour,
                 local.tm_min,
                 local.tm_sec))
    dirname = '%04d-%02d-%02d' % (local.tm_year,
                 local.tm_mon,
                 local.tm_mday)
    dirname = os.path.join(SNAPSHOT_DIR, dirname)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    os.chdir(dirname)
    save_screen(filename)


def main():
    os.chdir(SNAPSHOT_DIR)
    while 1:
        save_current()
        time.sleep(PAUSE_SEC)


if __name__ == '__main__':
    main()

