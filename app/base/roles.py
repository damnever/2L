# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import


class Roles(object):
    # head of the site
    Root = 'root'
    Admin = 'admin'
    TopicCreation = 'topic_creation'
    Vote = 'vote'
    Comment = 'comment'
    TopicEdit = 'topic:{0}:edit'
    PostEdit = 'post:{0}:edit'
