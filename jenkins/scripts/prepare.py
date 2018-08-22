#!/usr/bin/env python

import sys
import os
import glob
import subprocess

def apk_to_jar(file_name):
    print 'dex2jar: %s' % file_name

    if subprocess.call(['/scripts/dex2jar-2.0/d2j-dex2jar.sh', file_name]) != 0:
        print '[!] Could not convert %s to .jar' % file_name


def unzip(file_name, delete=True):
    print 'unzip: %s' % file_name

    if subprocess.call(['unzip', file_name]) == 0:
        if delete:
            os.remove(file_name)

        # if the zip file contains .apk, prepare them too
        prepare_files()
    else:
        print '[!] Could not convert %s to .jar' % file_name


def prepare_files():
    for file_name in glob.glob('*'):
        ext = os.path.splitext(file_name)[1].lower()

        if ext == '.apk':
            apk_to_jar(file_name)

        elif ext == '.zip':
            unzip(file_name)

        elif ext == '.war':
            unzip(file_name, False)
            subprocess.call(['mv', file_name, file_name + '.jar'])

        elif ext == '.ear':
            unzip(file_name, True)
            subprocess.call(['mv', file_name, file_name + '.jar'])

if __name__ == '__main__':
    prepare_files()
