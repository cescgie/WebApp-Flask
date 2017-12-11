# This file defines command line commands for manage.py
#
# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

import datetime

from flask import current_app, json
from flask_script import Command

from app import db
from app.models.user_models import User, Role, Paper

from phpserialize import serialize

class InitDbCommand(Command):
    """ Initialize the database."""

    def run(self):
        init_db()

def init_db():
    """ Initialize the database."""
    db.drop_all()
    db.create_all()
    create_users()
    create_papers()

def create_users():
    """ Create users """

    # Create all tables
    db.create_all()

    # Adding roles
    admin_role = find_or_create_role('admin', u'Admin')
    reviewer_role = find_or_create_role('reviewer', u'Reviewer')

    # Add users
    find_or_create_user(u'Admin', u'Example', u'admin@example.com', 'Password1', admin_role)
    find_or_create_user(u'Reviewer1', u'Example', u'reviewer1@example.com', 'Password1', reviewer_role)
    find_or_create_user(u'Reviewer2', u'Example', u'reviewer2@example.com', 'Password1', reviewer_role)
    find_or_create_user(u'Reviewer3', u'Example', u'reviewer3@example.com', 'Password1', reviewer_role)
    find_or_create_user(u'Member1', u'Example', u'member1@example.com', 'Password1')
    find_or_create_user(u'Member2', u'Example', u'member2@example.com', 'Password1')
    find_or_create_user(u'Member3', u'Example', u'member3@example.com', 'Password1')

    # Save to DB
    db.session.commit()


def find_or_create_role(name, label):
    """ Find existing role or create new role """
    role = Role.query.filter(Role.name == name).first()
    if not role:
        role = Role(name=name, label=label)
        db.session.add(role)
    return role


def find_or_create_user(first_name, last_name, email, password, role=None):
    """ Find existing user or create new user """
    user = User.query.filter(User.email == email).first()
    if not user:
        user = User(email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=current_app.user_manager.hash_password(password),
                    active=True,
                    confirmed_at=datetime.datetime.utcnow())
        if role:
            user.roles.append(role)
        db.session.add(user)
    return user

def create_papers():
    create_papers_func(serialize([5]),'Title 5', 'Abstract 5',5)
    create_papers_func(serialize([4,6]),'Title 6', 'Abstract 6',6)
    create_papers_func(serialize([7]),'Title 7', 'Abstract 7',7)

    db.session.commit()

def create_papers_func(authors,title,abstract,submittedBy,status=0,mediaRef=None,mediaTyp=None):
    paper = Paper(authors=authors,
                title=title,
                abstract=abstract,
                mediaRef=mediaRef,
                mediaTyp=mediaTyp,
                status=status,
                submittedBy=submittedBy)
    db.session.add(paper)


