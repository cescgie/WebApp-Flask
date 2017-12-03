# Installation
- If there is no virtualenv yet , create one
    `virtualenv env`
- Activate virtualenv
    `source env/bin/activate`
- Install requirements
    `pip install -r requirements`
- Create DB tables and populate the roles and users tables
    `python manage.py init_db`
- Run with debug
    `python manage.py runserver`