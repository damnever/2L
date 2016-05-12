# -*- coding: utf-8 -*-
"""
Reference: pystatsd.statsd
Just for numbers of code line, O(∩_∩)O~, I am a genius...
"""
from __future__ import print_function, division, absolute_import

import socket
import time
import random


class Client(object):

    def __init__(self, host='localhost', port=8125, prefix='2L'):
        self._addr = (host, port)
        self._prefix = prefix
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                                   socket.IPPROTO_UDP)

    def timing_since(self, stat, start, sample_rate=1):
        """Log timing information as the number of microseconds
        since the provided time float.
        """
        self.timing(stat, int((time.time()-start) * 1000000), sample_rate)

    def timing(self, stat, time, sample_rate=1):
        """Log timing information for a single stat."""
        stats = {stat: "%f|ms" % time}
        self.send(stats, sample_rate)

    def gauge(self, stat, value, sample_rate=1):
        """Log gauge information for a single stat."""
        stats = {stat: "%f|g" % value}
        self.send(stats, sample_rate)

    def increment(self, stats, sample_rate=1):
        """Increments one or more stats counters."""
        self.update_stats(stats, 1, sample_rate=sample_rate)

    def decrement(self, stats, sample_rate=1):
        """Decrements one or more stats counters."""
        self.update_stats(stats, -1, sample_rate=sample_rate)

    incr = increment
    decr= decrement

    def update_stats(self, stats, delta, sample_rate=1):
        """Updates one or more stats counters by arbitrary amounts."""
        if not isinstance(stats, list):
            stats = [stats]
        data = dict((stat, "%s|c" % delta) for stat in stats)
        self.send(data, sample_rate)

    def send(self, data, sample_rate=1):
        """Squirt the metrics over UDP."""
        if self._prefix:
            data = dict((".".join((self._prefix, stat)), value)
                        for stat, value in data.items())

        if sample_rate < 1:
            if random.random() > sample_rate:
                return
            sampled_data = dict((stat, "%s|@%s" % (value, sample_rate))
                                for stat, value in data.items())
        else:
            sampled_data = data

        self._sock.sendto(
            '\n'.join("%s:%s" % (stat, value)
                      for stat, value in sampled_data.iteritems()),
            self._addr)


statsd_client = Client()
