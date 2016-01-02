# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import click

from app.app import run_server
from app.libs.db import init_db, drop_db


@click.group()
def main():
    pass


@main.command()
@click.option('--host', default='127.0.0.1',
              help='run server at the given host')
@click.option('--port', default=8888,
              help='run server on the given port')
def runserver(host, port):
    """Run 2L services."""
    click.echo(('[2L] The services running at: '
                'http://{0}:{1}/').format(host, port))
    run_server(port)


@main.command()
def initdb():
    """Initialize MySQL databse."""
    click.echo('[2L] {0}..'.format(initdb.__doc__))
    init_db()


@main.command()
def dropdb():
    """Drop MySQL database."""
    click.echo('[2L] {0}..'.format(dropdb.__doc__))
    drop_db()
