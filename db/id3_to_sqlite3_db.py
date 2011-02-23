#!/usr/bin/python
# -*- coding: cp1252 -*-
import os
import sys
import getopt
import sqlite3
import id3reader as ID3

__doc__ = "Generate m3u playlists (default: local dir)"
__author__ = "Lawrence Oluyede <l.oluyede@gmail.com>"
__date__ = "Jul 12 2004"
__version__ = "0.2"

"""
A simple m3u file is like this:

#EXTM3U
#EXTINF:111,Coldplay - In Myplace
/path/to/the/song/Coldplay - In My Place.mp3

- #EXTM3U is the format descriptor (unchanging)
- #EXTINF is the record marker (with extended info, unchanging)
- : is the separator
- 111 is the length of the track in whole seconds
- , is the other separator
- the name of the track (a good generator parses the ID3,
  if there isn't an ID3 use the file name without the extension)
- /path/etc. etc. is the absolute (or relative) path to the file name
  of the track

Requirements:

- Python 2.2
- pymad for track length - http://spacepants.org/src/pymad/
- id3-py for reading ID3 infos - http://id3-py.sourceforge.net/

"""

FORMAT_DESCRIPTOR = "#EXTM3U"
RECORD_MARKER = "#EXTINF"


def _usage():
    """ print the usage message """
    msg = "Usage:  pyM3U.py [options] playlist_name [path]\n"
    msg += __doc__ + "\n"
    msg += "Options:\n"
    msg += "%5s,\t%s\t\t%s\n" % ("-n", "--no-sort", "do not sort entries by filename")
    msg += "%5s,\t%s\t\t\t%s\n" % ("-w", "--walk", "walk into subdirs (default: no walk)")
    msg += "\n%5s,\t%s\t\t\t%s\n\n" % ("-h", "--help", "display this help and exit")

    print msg

def generate_list(name="songs_list.m3u", path=".",
                  sort=True, walk=False):
    """ generates the M3U playlist with the given file name

    and in the given path """
    db = sqlite3.connect('newdev.db')
    cursor = db.cursor()

    cursor.execute("""
drop table if exists songs;
""")

    db.commit()
    cursor.execute("""
CREATE TABLE songs (
  `id` INTEGER PRIMARY KEY,
  `artist` varchar(100) NOT NULL,
  `album` varchar(100) NOT NULL,
  `genre` int(10) NOT NULL,
  `title` varchar(100) NOT NULL,
  `track` varchar(200) NOT NULL,
  `comment` varchar(100) NULL,
  `year` varchar(10) NOT NULL,
  `location` varchar(200) NOT NULL
);
""")

    db.commit()
    cursor.execute("""
drop table if exists artists;
""")

    db.commit()
    cursor.execute("""
CREATE TABLE artists (
  `id` INTEGER PRIMARY KEY,
  `artist` varchar(100) NOT NULL,
  `album` varchar(100) NOT NULL,
  `genre` int(10) NOT NULL,
  `title` varchar(100) NOT NULL,
  `track` varchar(200) NOT NULL,
  `comment` varchar(100) NULL,
  `year` varchar(10) NOT NULL,
  `location` varchar(200) NOT NULL
);
""")

    db.commit()
    cursor.execute("""
CREATE UNIQUE INDEX artists_indx ON artists (artist) ;
""")

    db.commit()
    cursor.execute("""
drop table if exists genres;
""")

    db.commit()
    cursor.execute("""
CREATE TABLE genres (
  `id` INTEGER PRIMARY KEY,
  `artist` varchar(100) NOT NULL,
  `album` varchar(100) NOT NULL,
  `genre` int(10) NOT NULL,
  `title` varchar(100) NOT NULL,
  `track` varchar(200) NOT NULL,
  `comment` varchar(100) NULL,
  `year` varchar(10) NOT NULL,
  `location` varchar(200) NOT NULL
);
""")

    db.commit()
    cursor.execute("""
CREATE UNIQUE INDEX genres_indx ON genres (genre) ;
""")

    db.commit()
    fp = None
    try:
        try:
            if walk:
                # recursive version
                mp3_list = [os.path.join(root, i) for root, dirs, files in os.walk(path) for i in files \
                            if i[-3:] == "mp3" or i[-3:] == "MP3"]
            else:
                # non recursive version
                mp3_list = [i for i in os.listdir(path) if i[-3:] == "mp3" or i[-3:] == "MP3"]

            #print mp3_list

            if sort:
                mp3_list.sort()

            fp = file(name, "w")
            fp.write(FORMAT_DESCRIPTOR + "\n")

            for track in mp3_list:
                print track
                if not walk:
                    track = os.path.join(path, track)
                else:
                    track = os.path.abspath(track)
                # open the track with mad and ID3
                #mf = mad.MadFile(track)
                id3info = ID3.Reader(track)
                print id3info.getValue('TT2')
                # M3U format needs seconds but
                # total_time returns milliseconds
                # hence i convert them in seconds
                #track_length = mf.total_time() / 1000

                # get the artist name and the title
                album = id3info.getValue('album')
                artist = id3info.getValue('performer')
                title = id3info.getValue('title')
                id3track = id3info.getValue('track')
                year = id3info.getValue('year')
                genre = id3info.getValue('genre')
                comment = id3info.getValue('comment')
                location = track
                artist = "%s" % artist
                title = "%s" % title
                if id3track :
                    id3track = id3track.replace("'", "''")
                if artist :
                    artist = artist.replace("'", "''")
                    #artist = artist.replace('\xe4', "")
                if year :
                    year = year.replace("'", "''")
                if album :
                    album = album.replace("'", "''")
                    album = album.replace("(", "")
                    album = album.replace(")", "")
                    print '%s'%album
                    #quit()
                    #album = album.replace('\xe4', "")
                if title :
                    title = title.replace("'", "''")
                if genre :
                    genre = genre.replace("'", "''")
                if location :
                    location = location.replace("'", "''")
                if track :
                    track = track.replace("\\", "/")
                    track = track.replace("'", "''")
                    #title = title.replace('\xe4', "")
                if comment :
                    comment = comment.replace("\\", "\\\\")
                    comment = comment.replace("'", "\\'")
                    comment = comment.replace('\xe4', "")
                    comment = comment.replace('\xa9', "")
                    comment = comment.replace('\xfe', "")
                    comment = comment.replace('\xad', "", 9)
                    comment = comment.replace('\xb4', "", 9)
                    comment = comment.replace('\x88', "", 9)
                    comment = comment.replace('\x99', "", 9)
                    comment = comment.replace('\xa8', "", 9)
                    comment = comment.replace('\xba', "", 9)
                    comment = comment.replace('\xac', "", 9)
                    comment = comment.replace('\xae', "", 9)
                    comment = comment.replace('\xc0', "", 9)
                    comment = comment.replace('\xc1', "", 9)
                    comment = comment.replace('\xc2', "", 9)
                    comment = comment.replace('\xc3', "", 9)
                    comment = comment.replace('\xc4', "", 9)
                    comment = comment.replace('\xc5', "", 9)
                    comment = comment.replace('\xc6', "", 9)
                    comment = comment.replace('\xc7', "", 9)
                    comment = comment.replace('\xc8', "", 9)
                    comment = comment.replace('\xc9', "", 9)
                    comment = comment.replace('\xca', "", 9)
                    comment = comment.replace('\xcb', "", 9)
                    comment = comment.replace('\xcc', "", 9)
                    comment = comment.replace('\x92', "", 9)
                    comment = comment.replace('\x9e', "", 9)
                    comment = comment.replace('\xf0', "", 9)
                    comment = comment.replace('\xf8', "", 9)
                    comment = comment.replace('\xf1', "", 9)
                    comment = comment.replace('\xe8', "", 9)
                    comment = comment.replace('\xd5', "", 9)
                    comment = comment.replace('\xd5', "", 9)
                    comment = comment.replace('\xfc', "", 9)
                    comment = comment.replace('\xfc', "", 9)
                    comment = comment.replace('\xeb', "", 9)
                    comment = comment.replace('\xb1', "", 9)
                    comment = comment.replace('\xe2', "", 9)
                    comment = comment.replace('\x8c', "", 9)
                    comment = comment.replace('\xfa', "", 9)
                    comment = comment.replace('\xd8', "", 9)
                    comment = comment.replace('\xd0', "", 9)
                    comment = comment.replace('\xd1', "", 9)
                    comment = comment.replace('\xd2', "", 9)
                    comment = comment.replace('\xd3', "", 9)
                    comment = comment.replace('\xd4', "", 9)
                    comment = comment.replace('\xd5', "", 9)
                    comment = comment.replace('\xd6', "", 9)
                    comment = comment.replace('\xd7', "", 9)
                    comment = comment.replace('\xb8', "", 9)
                    comment = comment.replace('\xbc', "", 9)
                    comment = comment.replace('\xd8', "", 9)
                    comment = comment.replace('\xce', "", 9)
                    comment = comment.replace('\xd4', "", 9)
                    comment = comment.replace('\xd5', "", 9)
                    comment = comment.replace('\xd6', "", 9)
                    comment = comment.replace('\xd7', "", 9)
                    comment = comment.replace('\xd8', "", 9)
                    comment = comment.replace('\xd9', "", 9)
                    comment = comment.replace('\xa3', "", 9)
                    comment = comment.replace('\x93', "", 9)
                    comment = comment.replace('\xf2', "", 9)
                    comment = comment.replace('\xf5', "", 9)
                    comment = comment.replace('\xaf', "", 9)
                    comment = comment.replace('\xa2', "", 9)
                    comment = comment.replace('\x90', "", 9)
                    comment = comment.replace('\x91', "", 9)
                    comment = comment.replace('\x92', "", 9)
                    comment = comment.replace('\x9b', "", 9)
                    comment = comment.replace('\x9d', "", 9)
                    comment = comment.replace('\x9f', "", 9)
                    comment = comment.replace('\xaa', "", 9)
                    comment = comment.replace('\xa1', "", 9)
                    comment = comment.replace('\xa2', "", 9)
                    comment = comment.replace('\xa3', "", 9)
                    comment = comment.replace('\xa4', "", 9)
                    comment = comment.replace('\xa5', "", 9)
                    comment = comment.replace('\xa6', "", 9)
                    comment = comment.replace('\xa7', "", 9)
                    comment = comment.replace('\xc9', "", 9)
                    comment = comment.replace('\xda', "", 9)
                    comment = comment.replace('\xdb', "", 9)
                    comment = comment.replace('\xdc', "", 9)
                    comment = comment.replace('\xe0', "", 9)
                    comment = comment.replace('\xe1', "", 9)
                    comment = comment.replace('\xe2', "", 9)
                    comment = comment.replace('\xe3', "", 9)
                    comment = comment.replace('\xe4', "", 9)
                    comment = comment.replace('\xea', "", 9)
                    comment = comment.replace('\xeb', "", 9)
                    comment = comment.replace('\xec', "", 9)
                    comment = comment.replace('\x8a', "", 9)
                    comment = comment.replace('\x8e', "", 9)
                    comment = comment.replace('\x84', "", 9)
                    comment = comment.replace('\xc6', "", 9)
                    comment = comment.replace('\xbf', "", 9)
                    comment = comment.replace('\xff', "", 9)
                    comment = comment.replace('\xf1', "", 9)
                    comment = comment.replace('\xf2', "", 9)
                    comment = comment.replace('\xf3', "", 9)
                    comment = comment.replace('\xf4', "", 9)
                    comment = comment.replace('\xf5', "", 9)
                    comment = comment.replace('\xf6', "", 9)
                    comment = comment.replace('\xf7', "", 9)
                    comment = comment.replace('\xf8', "", 9)
                    comment = comment.replace('\x94', "", 9)
                    comment = comment.replace('\xb2', "", 9)
                    comment = comment.replace('\xa7', "", 9)
                    comment = comment.replace('\x82', "", 9)
                    comment = comment.replace('\xb9', "", 9)
                if genre :
                    genre = genre.replace("(", "")
                    genre = genre.replace(")", "")

                # if artist and title are there
                #if artist and title:
                    #fp.write(RECORD_MARKER + ":" + str(track_length) + "," +\
                               #artist + " - " + title + "\n")
                #else:
                    #fp.write(RECORD_MARKER + ":" + str(track_length) + "," +\
                               #os.path.basename(track)[:-4] + "\n")
                print "'artist: %s'" % (artist)
                print "'album: %s'" % (album)
                print "'genre: %s'" % (genre)
                print "'title: %s'" % (title)
                print "'track: %s'" % (id3track)
                print "'comment: %s'" % (comment)
                print "'year: %s'" % (year)
                print "'Location: %s'" % (location)
                q = "select count(id) from songs where artist=\'%s\' and album=\'%s\' and  genre=\'%s\' and title=\'%s\'  and year=\'%s\'" % (artist , album , genre , title, year)
                print q
                cursor.execute (q)
                db.commit()
                row = cursor.fetchone ()
                print "count:", row[0]
                #count = row[0]
                count = 0
                if count == 0:
                    q = "INSERT INTO songs (\'artist\' ,\'album\' ,\'genre\' ,\'title\' ,\'track\'  ,\'year\',\'location\') VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\',  \'%s\', '%s')" % (artist , album , genre , title , id3track ,  year, location)
                    print q
                    #quit ()
                    cursor.execute (q)
                    db.commit()
                    # insert artist if unique
                    q = "select count(id) from artists where artist=\'%s\'" % (artist)
                    print q
                    cursor.execute (q)
                    db.commit()
                    row = cursor.fetchone ()
                    print "count:", row[0]
                    count = row[0]
                    if count == 0:
                        q = "INSERT INTO artists (\'artist\' ,\'album\' ,\'genre\' ,\'title\' ,\'track\'  ,\'year\',\'location\') VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\',  \'%s\', '%s')" % (artist , album , genre , title , id3track ,  year, location)
                        print q
                        #quit ()
                        cursor.execute (q)
                        db.commit()

                    # insert genre if unique
                    q = "select count(id) from genres where genre=\'%s\'" % (genre)
                    print q
                    cursor.execute (q)
                    db.commit()
                    row = cursor.fetchone ()
                    print "count:", row[0]
                    count = row[0]
                    if count == 0:
                        q = "INSERT INTO genres (\'artist\' ,\'album\' ,\'genre\' ,\'title\' ,\'track\'  ,\'year\',\'location\') VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\',  \'%s\', '%s')" % (artist , album , genre , title , id3track ,  year, location)
                        print q
                        #quit ()
                        cursor.execute (q)
                        db.commit()
                # write the fullpath
                fp.write(track + "\n")

        except (OSError, IOError), e:
            print e
    finally:
        if db:
            db.commit()
        if fp:
            fp.close()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.stderr.write("No playlist name given\n")
        sys.exit(1)

    options = "nhw"
    long_options = ["no-sort", "help", "walk"]

    try:
        opts, args = getopt.getopt(sys.argv[1:], options, long_options)
    except getopt.GetoptError:
        print "error"
        _usage()
        sys.exit(2)

    name, path, sort = "songs_list.m3u", ".", True
    walk = False

    #print opts, args

    # check cmd line args
    for o, a in opts:
        if o in ("-n", "--no-sort"):
            sort = False
        if o in ("-w", "--walk"):
            walk = True
        if o in ("-h", "--help"):
            _usage()
            sys.exit(1)

    try:
        name = args[0]
    except:
        pass

    try:
        path = args[1]
    except:
        pass

    #print name, path, sort

    if os.path.exists(path):
        generate_list(name, path, sort, walk)
    else:
        sys.stderr.write("Given path does not exist\n")
        sys.exit(2)
