# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import click


@click.group()
def main():
    pass


@main.command()
@click.option('--host', default='127.0.0.1',
              help='run server at the given host.')
@click.option('--port', default=9487,
              help='run server on the given port.')
def runserver(host, port):
    """Run 2L services."""
    from app.app import run_server

    click.echo(('[2L] The services running at: '
                'http://{0}:{1}/').format(host, port))
    run_server(host, port)


@main.command()
def initdb():
    """Initialize MySQL databse."""
    from app.libs.db import init_db
    from app.models import Permission, User, Topic
    from app.base.roles import Roles
    from app.settings import Admins, Topics
    from app.libs.utils import encrypt_password

    click.echo('[2L] {0}..'.format(initdb.__doc__))
    init_db()

    click.echo('\n\n[2L] init permisions...')
    for attr, role in Roles.__dict__.items():
        if (not attr.startswith('__') and '{0}' not in role and
                role != 'root'):
            click.echo(' -> {0}'.format(role))
            Permission.create(role)

    click.echo('\n\n[2L] init master chief...')
    bit_sum = Permission.root_permission()
    for admin in Admins:
        click.echo(' -> {0}'.format(admin))
        if admin['role'] == 'root':
            admin['role'] = bit_sum
        else:
            admin['role'] = (Permission.get_by_role(admin['role']).bit |
                             Permission.get_by_role('comment').bit |
                             Permission.get_by_role('vote').bit)
        admin['password'] = encrypt_password(admin['password'])
        User.create(**admin)

    click.echo('\n\n[2L] create default topics...')
    for topic in Topics:
        click.echo(' -> {0}'.format(topic))
        Topic.create(**topic)


@main.command()
def dropdb():
    """Drop MySQL database."""
    from app.libs.db import drop_db

    click.echo('[2L] {0}..'.format(dropdb.__doc__))
    drop_db()


@main.command()
def runtasks():
    """Run celery(task queue)."""
    import subprocess

    click.echo('[2L] {0}..'.format(runtasks.__doc__))
    cmd = ('celery worker --beat --autoscale=12,4 --app=app.tasks'
           ' --loglevel=warning --events --autoreload')
    subprocess.call(cmd.split())
