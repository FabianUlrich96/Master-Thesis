import re
import html
import urllib.request
from urllib.error import URLError, HTTPError
import urllib.parse
import math
import random
import string
import time


def unescape(text):
    parser = html
    return parser.unescape(text)


def prepare_translate(translation_object):
    if len(translation_object) < 5000:
        return True, translation_object
    else:
        n = int(math.ceil((len(translation_object)/5000)))
        chunk_len = len(translation_object)//n
        res = []

        for idx in range(0, len(translation_object), chunk_len):
            res.append(translation_object[idx: idx + chunk_len])
        return False, res


def translate(to_translate, to_language="auto", from_language="auto"):
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
            result = unescape(re_result[0])

        return result
    except HTTPError as err:
        print(err)
    except URLError as err:
        print(err)




def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def main():
    s1 = get_random_string(6000)

    to_translate = ["Hallo das ist noch ein Text", s1]

    for translation_object in to_translate:
        time.sleep(1)
        length_check, prepared_string = prepare_translate(translation_object)

        if length_check:
            translation = translate(translation_object, to_language="en")
            print(translation)
        else:
            translation = ['']
            for translation_string in prepared_string:
                translation_chunk = translate(translation_string, to_language="en")
                translation.append(translation_chunk)

            translation = ' '.join(translation)
            print(translation)


if __name__ == "__main__":
    main()
