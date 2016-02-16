# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from app.tasks.celery import app


@app.task(name='update_permission', max_retries=5)
def update_permission(user, role):
    from app.libs.db import db_session
    from app.models import Permission

    user.role |= Permission.get_by_role(role).bit
    db_session.add(user)
    db_session.commit()


@app.task(name='check_proposal', max_retries=5)
def check_proposal(topic_id):
    from app.libs.db import db_session
    from app.models import Topic, User, Permission, TopicUpVote, TopicDownVote
    from app.base.roles import Roles

    user_count = User.count()
    topic = Topic.get(topic_id)
    user = User.get(topic.admin_id)
    up_votes = TopicUpVote.count_by_topic(topic_id)
    down_votes = TopicDownVote.count_by_topic(topic_id)

    # Check if the proposal can be accepted or rejected.
    if (up_votes - down_votes) > (user_count / 2):
        topic.state = 1
        # Update permission.
        permission = Roles.TopicEdit.format(topic.name)
        p = Permission.create(permission)
        user.role |= p.bit
        db_session.add(user)
    else:
        topic.state = -1

    db_session.add(topic)
    db_session.commit()


@app.task(name='send_email', max_retries=4)
def send_email(to_name, to_addr, subject, message):
    pass


@app.task(name='', max_retries=10)
def notifiy():
    pass
