# Peer Review System
Flask application for Peer Review System based on [Flask-User starter app](https://github.com/lingthio/Flask-User-starter-app.git)

## Starter
- If there is no virtualenv yet , create one<br>
    `virtualenv env`
- Activate virtualenv<br>
    `source env/bin/activate`
- Install requirements<br>
    `pip install -r requirements.txt`
- Create DB tables and populate the roles and users tables<br>
    `python manage.py init_db`
- Run with debug<br>
    `python manage.py runserver`

## Development
- Activate virtualenv<br>
    `source env/bin/activate`
- Run with debug<br>
    `python manage.py runserver`

## Test User Credentials
- Admin or Conference chair<br>
    `admin@example.com:Password1`
- Reviewer<br>
    `reviewer1@example.com:Password1`
- Normal User<br>
    `member1@example.com:Password1`

## TASKS
1. There should be a registration page. The user is identified by their email address, and
must provide a password of their choice.
2. There should be a page for the Conference Chair to assign some of the registered users to
be reviewers of the conference.
3. There should be a paper submission page. Any registered user may submit papers. A paper
has one or more authors, all authors need to be registered. A paper also has a title and an
abstract. File upload is not required in this lab. A user may submit any number of papers.
4. There should be a page for the Conference Chair to assign the papers to reviewers. Usually,
each paper is assigned to three reviewers. It should be avoided that an author gets their
own paper to review.
5. There should be a page for a reviewer to upload their review. In this lab, the reviewer only
gives the paper a score, which is an integer between −2 and 2, −2 being the worst score
(totally unacceptable), 2 the best (great paper ).
6. There should be a page for the Conference Chair to have an overview of the scores, and
makes final decisions of acceptance or rejection of the papers.
7. There should be a page for user login. Paper submission, review submission, and assignment
of reviewers should be protected by access control.
8. After successful login, some messages should be displayed to the user, including a list of
the papers for the user to review, status (“under review”/“accepted”/“rejected”) of the
user’s co-authored papers. An author is not allowed to see the IDs of the reviewers of their
papers
