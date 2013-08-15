#!/usr/bin/python

'''
A utility script for processing all images in the current directory by 
resizing them and then sorting them into subdirectories.
'''

import glob
import os

import exifread


def date_to_dir_name(date):
    '''
    Given an EXIF date, return the directory name the file should be moved to.
    '''
    months = {
        1 : "Jan",
        2 : "Feb",
        3 : "Mar",
        4 : "Apr", 
        5 : "May",
        6 : "Jun",
        7 : "Jul",
        8 : "Aug", 
        9 : "Sep",
        10 : "Oct",
        11 : "Nov",
        12 : "Dec"
        }

    ymd = date.split()[0]
    (year, month, day) = ymd.split(":")
    month = months[int(month)]
    return "%s %s" % (month, year)


def find_all_pictures():
    '''
    Find all pictures of interest in the current directory & return as a list
    '''
    result = []
    for filename in glob.glob("*"):
        _, ext = os.path.splitext(filename)
        if ext.lower()[1:] in ['jpg', 'jpeg']:
            result.append(filename)
    return result


def move_pictures(pictures):
    '''
    Move all pictures in the supplied list into folders based upon the month 
    & year the picture was taken as reported by the picture's EXIF data.
    '''
    for fname in pictures: 
        with open(fname) as fobj:
            tags = exifread.process_file(fobj)
            if tags.has_key('EXIF DateTimeOriginal'):
                dirname = date_to_dir_name(tags['EXIF DateTimeOriginal'].values)
                try:
                    os.mkdir(dirname)
                except OSError as e:
                    pass  # directory already exists

                newname = os.path.join(dirname, fname) 
                os.rename(fname, newname) 
                print("Moved %s to %s" % (fname, newname))
            else:
                print("Failed to move %s, could not read date from EXIF data" % fname)


def resize_pictures(files):
    '''
    Resize each picture in files to 1920x1080 resolution (preserving aspect ratio)
    '''
    for fname in files:
        command = 'convert "%s" -resize 1920x1080 "%s"' % (fname, fname)
        result = os.system(command)
        if result != 0:
            print("Failed to resize %s, got errcode %s" % (fname, result))
        else:
            print("Resized %s" % fname)


def main():
    pictures = find_all_pictures()
    resize_pictures(pictures)
    move_pictures(pictures)


if __name__=="__main__":
    main()
