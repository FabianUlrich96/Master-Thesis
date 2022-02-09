from database.models import Apis, Jobs, VideoList, CommentList
from app_config import ma


class ApisSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Apis


class JobsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Jobs


class VideoListSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = VideoList


class CommentListSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CommentList
