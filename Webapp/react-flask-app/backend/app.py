from flask_cors import CORS
import logger
from app_config import app, db
from routes.apis_route import apis_blueprint
from routes.jobs_route import jobs_blueprint
from routes.videolist_route import videos_blueprint
from routes.commentlist_route import comments_blueprint
log = logger.create_logger(__name__)
db.create_all()
CORS(app)

app.register_blueprint(apis_blueprint)
app.register_blueprint(jobs_blueprint)
app.register_blueprint(videos_blueprint)
app.register_blueprint(comments_blueprint)


if __name__ == '__main__':
    app.run(host='0.0.0.0')

