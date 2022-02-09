from app_config import db
from sqlalchemy.orm import backref


class Apis(db.Model):
    name = db.Column(db.String(200), primary_key=True)
    token = db.Column(db.String(50))
    service = db.Column(db.String(50))

    def __init__(self, name, token, service):
        self.name = name
        self.token = token
        self.service = service


class Jobs(db.Model):
    job_id = db.Column('job_id', db.Integer, primary_key=True)
    job_type = db.Column(db.String(50))
    api = db.Column(db.String(100), db.ForeignKey('apis.name'))
    api_backref = db.relationship("Apis", backref=backref("apis", uselist=False))
    name = db.Column(db.String(100))
    date = db.Column(db.Date)
    query = db.Column(db.String(200))
    done = db.Column(db.Boolean)
    failed = db.Column(db.Boolean)
    state = db.Column(db.Float)

    def __init__(self, job_id, job_type, api, name, date, query, done, failed, state):
        self.job_id = job_id
        self.job_type = job_type
        self.api = api
        self.name = name
        self.date = date
        self.query = query
        self.done = done
        self.failed = failed
        self.state = state


class VideoList(db.Model):
    video_id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(50))
    job = db.Column(db.Integer, db.ForeignKey(Jobs.job_id))
    job_backref = db.relationship("Jobs", backref=backref("jobs", uselist=False))

    def __init__(self, video_id, kind, job):
        self.video_id = video_id
        self.kind = kind
        self.job = job


class CommentList(db.Model):
    video_id = db.Column(db.Integer, db.ForeignKey(VideoList.video_id), primary_key=True)
    comment = db.Column(db.Text)
    job = db.Column(db.Integer, db.ForeignKey('jobs.job_id'))

    def __init__(self, video_id, comment, job):
        self.video_id = video_id
        self.comment = comment
        self.job = job


