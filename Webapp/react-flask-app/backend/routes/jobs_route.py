from app_config import db
from flask import request, jsonify, Blueprint
from database.models import Jobs
from database.schemas import JobsSchema
import logger
log = logger.create_logger(__name__)
job_schema = JobsSchema()
jobs_schema = JobsSchema(many=True)
jobs_blueprint = Blueprint('jobs_blueprint', __name__, template_folder='templates')


@jobs_blueprint.route('/jobs', methods=['GET', 'POST', 'DELETE'])
def jobs_all():
    if request.method == 'GET':
        jobs = db.session.query(Jobs).all()
        return jsonify(jobs_schema.dump(jobs))

    if request.method == 'POST':
        print('post things')
    if request.method == 'DELETE':
        print('job deleted')
    else:
        log.error('405 Method Not Allowed')


@jobs_blueprint.route('/jobs/<job_id>', methods=['GET', 'POST', 'DELETE'])
def jobs_id(job_id):
    if request.method == 'GET':
        return job_id
    if request.method == 'POST':
        print('post things')
    if request.method == 'DELETE':
        print('job deleted')
    else:
        log.error('405 Method Not Allowed')