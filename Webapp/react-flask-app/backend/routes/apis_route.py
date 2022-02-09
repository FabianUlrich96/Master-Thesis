from app_config import db
from flask import request, jsonify, Blueprint
from database.models import Apis
from database.schemas import ApisSchema
import logger
import pandas as pd
from sqlalchemy.exc import IntegrityError
log = logger.create_logger(__name__)
api_schema = ApisSchema()
apis_schema = ApisSchema(many=True)
apis_blueprint = Blueprint('apis_blueprint', __name__, template_folder='templates')


@apis_blueprint.route('/apis', methods=['GET', 'POST', 'DELETE'])
def apis_all():
    if request.method == 'GET':
        apis = db.session.query(Apis).all()
        return jsonify(apis_schema.dump(apis))

    if request.method == 'POST':
        data = request.json
        try:
            apis_df = pd.DataFrame(data, index=[0])
            apis_df.to_sql('apis', con=db.engine, if_exists='append', chunksize=1000, index=False)
        except IntegrityError as e:
            log.error(e)
        return 'Ok'
    if request.method == 'DELETE':
        print('job deleted')
    else:
        log.error('405 Method Not Allowed')


@apis_blueprint.route('/apis/<api_id>', methods=['GET', 'POST', 'DELETE'])
def apis_id(api_id):
    if request.method == 'GET':
        return api_id
    if request.method == 'POST':
        log.info(api_id)
    if request.method == 'DELETE':
        print('job deleted')
    else:
        log.error('405 Method Not Allowed')