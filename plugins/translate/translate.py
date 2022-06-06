import requests
import hashlib
import random
from config import bd_appid, bd_key


def bd_trans(query, lang_to):
    salt = random.randint(0,1000)
    lang_from = 'auto'
    sign = hashlib.md5(f'{bd_appid}{query}{salt}{bd_key}'.encode('utf8')).hexdigest()

    params = {
        'q': query,
        'from': lang_from,
        'to': lang_to,
        'appid': bd_appid,
        'salt': salt,
        'sign': sign
    }

    url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'

    try:
        resp_info = requests.get(url=url, params=params).json()
        result = resp_info['trans_result'][0]['dst']
        return result
    except:
        return '翻译出错了!'


if __name__ == '__main__':
    print(bd_trans('苹果', 'en'))