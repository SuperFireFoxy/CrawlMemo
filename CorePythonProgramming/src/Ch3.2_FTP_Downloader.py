#! /usr/bin/python
import ftplib
import os
import socket

HOST = 'ftp.opera.com'
DIRN = 'pub/opera/unix/1060b1/'
FILE = 'opera-10.60-6368.i386.freebsd.tar.bz2'


def main():
    try:
        f = ftplib.FTP(HOST)
    except(socket.error, socket.gaierror) as e:
        print('ERROR: can not reach %' % HOST)
    print('***Connected to host %s' % HOST)

    try:
        f.login()
    except ftplib.error_perm:
        print('ERROR: can not login anonymously')
        return
    print('***Login as anonymous')

    try:
        f.cwd(DIRN)
    except ftplib.error_perm:
        print('ERROR: can not CD to %s' % DIRN)
        return
    print('***Changed to %s folder' % DIRN)

    try:
        f.retrbinary('RETR %s' % FILE, open(FILE, 'wb').write)
    except ftplib.error_perm:
        print('ERROR: cannot read file "%s"' % FILE)
        os.unlink(FILE)
        return
    print('***Downloaded "%s" to CWD' % FILE)

    f.quit()


if __name__ == '__main__':
    main()
