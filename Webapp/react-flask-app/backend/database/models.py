from app_config import db
from sqlalchemy.orm import backref


class Users(db.Model):
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.Text)
    date_created = db.Column(db.Date)


class Apis(db.Model):
    name = db.Column(db.String(200), primary_key=True)
    token = db.Column(db.String(50))
    service = db.Column(db.String(50))

    def __init__(self, name, token, service):
        self.name = name
        self.token = token
        self.service = service


class Jobs(db.Model):
    job_id = db.Column('job_id', db.Integer, primary_key=True, autoincrement=True)
    job_type = db.Column(db.String(50))
    api = db.Column(db.String(100), db.ForeignKey('apis.name'))
    api_backref = db.relationship("Apis", backref=backref("apis", uselist=False))
    name = db.Column(db.String(100))
    date = db.Column(db.Date)
    query = db.Column(db.String(200))
    published_before = db.Column(db.Date)
    published_after = db.Column(db.Date)
    done = db.Column(db.Boolean)
    failed = db.Column(db.Boolean)

    def __init__(self, job_id, job_type, api, name, date, query, done, published_before, published_after, failed):
        self.job_id = job_id
        self.job_type = job_type
        self.api = api
        self.name = name
        self.date = date
        self.query = query
        self.published_before = published_before
        self.published_after = published_after
        self.done = done
        self.failed = failed


class VideoList(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    video_id = db.Column(db.String(50))
    kind = db.Column(db.String(50))
    job = db.Column(db.Integer, db.ForeignKey(Jobs.job_id))
    job_backref = db.relationship("Jobs", backref=backref("jobs", uselist=False))
    page = db.Column(db.String(50))
    date = db.Column(db.Date)

    def __init__(self, id, video_id, kind, job, page, date):
        self.id = id
        self.video_id = video_id
        self.kind = kind
        self.job = job
        self.page = page
        self.date = date


class CommentList(db.Model):
    video_id = db.Column(db.String(50), primary_key=True)
    job = db.Column(db.Integer, db.ForeignKey('jobs.job_id'))
    page = db.Column(db.Text)
    date = db.Column(db.Date)
    author = db.Column(db.Text)
    likes = db.Column(db.Integer)
    published = db.Column(db.Date)
    updated = db.Column(db.Date)
    reply_count = db.Column(db.Integer)
    comment_id = db.Column(db.String(50))
    comment = db.Column(db.Text)

    def __init__(self, video_id, job, page, date, author, likes, published, updated, reply_count, comment_id, comment):
        self.video_id = video_id
        self.job = job
        self.page = page
        self.date = date
        self.author = author
        self.likes = likes
        self.published = published
        self.updated = updated
        self.reply_count = reply_count
        self.comment_id = comment_id
        self.comment = comment


class ReplyList(db.Model):
    video_id = db.Column(db.String(50), primary_key=True)
    job = db.Column(db.Integer, db.ForeignKey('jobs.job_id'))
    page = db.Column(db.Text)
    date = db.Column(db.Date)
    parent_id = db.Column(db.String(50))
    author = db.Column(db.Text)
    likes = db.Column(db.Integer)
    published = db.Column(db.Date)
    updated = db.Column(db.Date)
    comment = db.Column(db.Text)

    def __init__(self, video_id, job, page, date, parent_id, author, likes, published, updated, comment):
        self.video_id = video_id
        self.job = job
        self.page = page
        self.date = date
        self.parent_id = parent_id
        self.author = author
        self.likes = likes
        self.published = published
        self.updated = updated
        self.comment = comment



