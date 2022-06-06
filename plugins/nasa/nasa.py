import requests
from utils import gen_date


def apod(api_key, date = gen_date('America/New_York')):
    url = 'https://api.nasa.gov/planetary/apod?api_key={}&date={}'.format(
        api_key, 
        date
    )

    try:
        rep = requests.get(url).json()
        if rep['media_type'] == 'image':
            outcome = '标题: {}\n[CQ:image,file={}]'.format(
                rep['title'],
                rep['hdurl']
            )
        elif rep['media_type'] == 'video':
            outcome = '标题: {}\n视频链接: {}'.format(rep['title'], rep['url'])
    except:
        outcome = '出错啦！'
    
    return outcome



if __name__ == '__main__':
    pass