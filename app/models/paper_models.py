from app import db


# Define the Paper data model
class Paper(db.Model):
    __tablename__ = 'papers'
    id = db.Column(db.Integer(), primary_key=True)
    authors = db.Column(db.String(255), nullable=False, server_default=u'') #user_id in array
    title = db.Column(db.String(255), nullable=False, server_default=u'')
    abstract = db.Column(db.String(255), nullable=False, server_default=u'')
    mediaRef = db.Column(db.String(255), server_default=u'')
    mediaTyp = db.Column(db.String(255), server_default=u'')
    status = db.Column(db.Integer(), server_default='0' ) #0=Submitted, 1=Under Review, 2=Accepted, 3=Rejected
    submittedBy = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))


# Define the Paper Reviewers association model
class PaperReviewers(db.Model):
    __tablename__ = 'paper_reviewers'
    id = db.Column(db.Integer(), primary_key=True)
    paper_id = db.Column(db.Integer(), nullable=False)
    reviewer_id = db.Column(db.Integer(), nullable=False)
    score = db.Column(db.Integer())