# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>


from flask import Blueprint, redirect, render_template
from flask import request, url_for
from flask_user import current_user, login_required, roles_accepted
from flask import Flask, jsonify

from app import db
from app.models.user_models import UserProfileForm, User, Role

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
    return render_template('member/paper_submission.html')

@main_blueprint.route('/member/list-papers')
@login_required # Limits access to authenticated users
def list_of_papers():
    return render_template('member/list_of_papers.html')

## User activation
@main_blueprint.route('/activate/user')
@roles_accepted('admin')
def activate_user_admin():
    id = request.args.get('id')
    active = request.args.get('active')

    activation = True if active == 'true' else False

    user = User.query.filter_by(id=id).update(dict(active=activation))
    db.session.commit()

    return jsonify({'activation':activation,'active':active})