# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import os
import sys
import fcntl
import errno


def already_running(pid_file):
    fd = os.open(pid_file, os.O_RDWR | os.O_CREAT, 0644)
    try:
        fcntl.lockf(fd, fcntl.LOCK_EX, 0, 0, os.SEEK_SET)
    except IOError as e:
        if e.errno == errno.EACCES or e.errno == errno.EAGAIN:
            return True
        raise
    else:
        os.ftruncate(fd, 0)
        os.write(fd, '{}'.format(os.getpid()))
        return False
    finally:
        os.close(fd)


def deamonize(entry, pid_file):
    os.umask(0)

    # Become a session leader to lose controlling TTY.
    pid = os.fork()
    if pid < 0:
        raise OSError('CAN NOT FORK!')
    elif pid != 0:
        sys.exit(0)
    os.setsid()

    # XXX: Ensure future opens won't allocate controlling TTY.

    pid = os.fork()
    if pid < 0:
        raise OSError('CAN NOT FORK!')
    elif pid != 0:
        sys.exit(0)

    fd0 = open('/dev/null', 'rw')
    fd1 = os.dup(0)
    fd2 = os.dup(0)
    if fd0 != 0 or fd1 != 1 or fd2 != 2:
        raise OSError('unexpected file description {0} {1} {2}'.format(
            fd0, fd1, fd2))

    # XXX: Initilaze the log file.

    entry()

    if already_running(pid_file):
        raise RuntimeError('Deamon already running!')
