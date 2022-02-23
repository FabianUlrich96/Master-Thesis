import logger
from app_config import db
from database.models import CommentList
from database.models import ReplyList
import re
import html
import urllib.request
from urllib.error import URLError, HTTPError
import urllib.parse
import math
import time

log = logger.create_logger(__name__)


class GoogleTranslate(object):
    def __init__(self, job_id, db):
        self.translator = None
        self.job_id = job_id
        self.db = db

    def unescape(self, text):
        parser = html
        return parser.unescape(text)

    def prepare_translate(self, translation_object):
        if len(translation_object) < 5000:
            return True, translation_object
        else:
            n = int(math.ceil((len(translation_object) / 5000)))
            chunk_len = len(translation_object) // n
            res = []

            for idx in range(0, len(translation_object), chunk_len):
                res.append(translation_object[idx: idx + chunk_len])
            return False, res

    def translate(self, to_translate, to_language="auto", from_language="auto"):
        agent = {'User-Agent':
                     "Mozilla/4.0 (\
                     compatible;\
                     MSIE 6.0;\
                     Windows NT 5.1;\
                     SV1;\
                     .NET CLR 1.1.4322;\
                     .NET CLR 2.0.50727;\
                     .NET CLR 3.0.04506.30\
                     )"}

        base_link = "http://translate.google.com/m?tl=%s&sl=%s&q=%s"

        to_translate = urllib.parse.quote(to_translate)
        link = base_link % (to_language, from_language, to_translate)
        try:
            request = urllib.request.Request(link, headers=agent)
            raw_data = urllib.request.urlopen(request).read()
            data = raw_data.decode("utf-8")
            expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
            re_result = re.findall(expr, data)

            if len(re_result) == 0:
                result = ""
            else:
                result = GoogleTranslate.unescape(self, re_result[0])

            return result
        except HTTPError as err:
            log.error(err)
        except URLError as err:
            log.error(err)

    def translate_text(self, comment_array, table):

        for translation_object in comment_array:
            time.sleep(1)
            length_check, prepared_string = self.prepare_translate(translation_object)

            if length_check:
                if table == "comment_list":
                    translation = self.translate(translation_object, to_language="en")
                    translation_db = CommentList.query.filter_by(comment=translation_object).first()
                    translation_db.translation = translation
                    db.session.commit()
                if table == "reply_list":
                    translation = self.translate(translation_object, to_language="en")
                    translation_db = ReplyList.query.filter_by(comment=translation_object).first()
                    translation_db.translation = translation
                    db.session.commit()
            else:
                translation = ['']
                for translation_string in prepared_string:
                    translation_chunk = self.translate(translation_string, to_language="en")
                    translation.append(translation_chunk)

                translation = ' '.join(translation)
                if table == "comment_list":
                    translation_db = CommentList.query.filter_by(comment=translation_object).first()
                    translation_db.translation = translation
                    db.session.commit()
                if table == "reply_list":
                    translation_db = ReplyList.query.filter_by(comment=translation_object).first()
                    translation_db.translation = translation
                    db.session.commit()
