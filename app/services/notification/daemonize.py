# -*- coding: utf-8 -*-

"""
Deamonize a program.
"""

from __future__ import print_function, division, absolute_import

import os
import fcntl
import errno
import signal


def daemonize_app(app, pid_file):
    """`app` must has `start` and `stop` method."""
    for m in ('start', 'stop'):
        if not hasattr(app, m):
            raise ValueError('`app` parameter has not `{0}` method.'.format(m))

    daemonize()

    if already_running(pid_file):
        raise RuntimeError('Deamon already running!')

    # Restore SIGHUP default.
    signal.signal(signal.SIGHUP, signal.SIG_DFL)

    def _sig_exit(signum, frame):
        app.stop()

    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGSTOP):
        signal.signal(sig, _sig_exit)

    app.start()


def already_running(pid_file):
    fd = os.open(pid_file, os.O_RDWR | os.O_CREAT | os.O_TRUNC, 0644)
    try:
        fcntl.lockf(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError as e:
        if e.errno in (errno.EACCES, errno.EAGAIN):
            return True
        raise
    else:
        os.write(fd, '{}'.format(os.getpid()))
        return False
    finally:
        os.close(fd)


def daemonize():
    # Clear file creation mask.
    os.umask(0)

    # Become a session leader to lose controlling TTY.
    pid = os.fork()
    if pid < 0:
        raise OSError('CAN NOT FORK!')
    elif pid != 0:
        os._exit(0)
    os.setsid()

    # XXX: Ensure future opens won't allocate controlling TTY.
    signal.signal(signal.SIGHUP, signal.SIG_IGN)

    pid = os.fork()
    if pid < 0:
        raise OSError('CAN NOT FORK!')
    elif pid != 0:
        os._exit(0)

    os.chdir('/')

    # Close all open file descriptors.
    for fd in (0, 1, 2):
        os.close(fd)
    # Then replace stdin, stdout, stderr with /dev/null.
    # XXX: or dup2
    fd0 = os.open(os.devnull, os.O_RDWR)
    fd1 = os.dup(0)
    fd2 = os.dup(0)
    if fd0 != 0 or fd1 != 1 or fd2 != 2:
        raise OSError('unexpected file description {0} {1} {2}'.format(
            fd0, fd1, fd2))

    # XXX: Initilaze the log file.
