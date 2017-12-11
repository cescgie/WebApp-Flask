# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>


from flask import Blueprint, redirect, render_template
from flask import request, url_for
from flask_user import current_user, login_required, roles_accepted
from flask import jsonify

from app import db
from app.forms.forms import PaperSubmissionForm
from app.models.paper_models import Paper
from app.models.user_models import UserProfileForm, User, Role, UsersRoles

from phpserialize import *
from io import StringIO

# When using a Flask app factory we must use a blueprint to avoid needing 'app' for '@app.route'
main_blueprint = Blueprint('main', __name__, template_folder='templates')


# The Home page is accessible to anyone
@main_blueprint.route('/')
def home_page():
    return render_template('pages/home_page.html')


# The User page is accessible to authenticated users (users that have logged in)
@main_blueprint.route('/member')
@login_required  # Limits access to authenticated users
def member_page():
    return render_template('pages/user_page.html')


# The Admin page is accessible to users with the 'admin' role
@main_blueprint.route('/admin')
@roles_accepted('admin')  # Limits access to users with the 'admin' role
def admin_page():
    return render_template('pages/admin_page.html')


@main_blueprint.route('/pages/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('main.home_page'))

    # Process GET or invalid POST
    return render_template('pages/user_profile_page.html',
                           form=form)


@main_blueprint.route('/conference/reviewer')
@roles_accepted('admin')  # Limits access to users with the 'admin' role
def assignment_of_reviewers():
    users = User.query.order_by(User.last_name).all()
    return render_template('conference/assignment_of_reviewers.html', 
                        users=users)


@main_blueprint.route('/conference/paper')
@roles_accepted('admin')  # Limits access to users with the 'admin' role
def assignment_papers_to_reviewers():
    return render_template('conference/assignment_papers_to_reviewers.html')


@main_blueprint.route('/conference/overview')
@roles_accepted('admin')  # Limits access to users with the 'admin' role
def overview_scores():
    return render_template('conference/overview_scores.html')


# ACCEPT: admin, reviewer
@main_blueprint.route('/reviewer/paper')
@roles_accepted('admin', 'reviewer')  # Limits access to admin and reviewer
def review_submission():
    return render_template('member/review_submission.html')


@main_blueprint.route('/member/submit-paper')
@login_required # Limits access to authenticated users
def paper_submission():
    form = PaperSubmissionForm(request.form)
    return render_template('member/paper_submission.html', form=form)


@main_blueprint.route('/member/list-papers')
@login_required # Limits access to authenticated users
def list_of_papers():
    papers = Paper.query.order_by(Paper.id).all()
    paper_authors = []
    for paper in papers:
        stream = StringIO(paper.authors)
        lists = dict_to_list(load(stream))
        author_names = []
        for author_id in lists:
            # Find user where id = author_id
            user = User.query.filter(User.id == author_id).first()
            # Convert unicode firstname to str
            # Push to author_names
            author_names.append(str(user.first_name))
        # Convert array to string separated with comma
        # Push to paper_authors
        paper_authors.append(', '.join(author_names))
    # List of status after index
    paper_status = ['Submitted', 'Under Review', 'Accepted', 'Rejected']
    return render_template('member/list_of_papers.html', 
                        papers=papers, 
                        paper_status=paper_status,
                        paper_authors=paper_authors)


# User activation
@main_blueprint.route('/activate/user')
@roles_accepted('admin')
def activate_user_admin():
    id = request.args.get('id')
    active = request.args.get('active')

    activation = True if active == 'true' else False

    user = User.query.filter_by(id=id).update(dict(active=activation))
    db.session.commit()

    return jsonify({'activation':activation,'active':active})


# User assignation as reviewer
@main_blueprint.route('/assign/user')
@roles_accepted('admin')
def assign_user_admin():
    id = request.args.get('id')
    user_role = UsersRoles.query.filter(UsersRoles.user_id == id).first()
    # Check if user role exist and prevent update admin role (role_id = 1)
    if user_role and user_role.role_id != 1:
            # Delete user role in UsersRoles
            db.session.delete(user_role)
            db.session.commit()
            action = 0
    else:
        # Update user role
        reviewer_role = find_or_create_role('reviewer', u'Reviewer')
        user = find_or_update_user(id, reviewer_role)
        action = 1

    return jsonify({'id':id,'action':action})


def find_or_create_role(name, label):
    """ Find existing role or create new role """
    role = Role.query.filter(Role.name == name).first()
    if not role:
        role = Role(name=name, label=label)
        db.session.add(role)
    return role


def find_or_update_user(id, role=None):
    """ Find existing user and update role """
    user = User.query.filter(User.id == id).first()
    if user and role:
        user.roles.append(role)
        db.session.commit()
    return user