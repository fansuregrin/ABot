import requests
from config import hefeng_key
from utils import gen_date


def get_weather_info(city):
    city_id = get_city_id(city)
    if not city_id:
        return f"出错了! {city}没有天气信息！"
    try:
        info = requests.get(f"https://devapi.heweather.net/v7/weather/now?location={city_id}&key={hefeng_key}").json()
        outcome = '城市：{}\n天气：{}\n温度：{}摄氏度\n体感温度：{}摄氏度\n{}{}级 风速: {}千米/小时\n相对湿度: {}%\n大气压强: {}百帕\n能见度: {}公里'.format(
            city,
            info["now"]["text"],
            info["now"]["temp"],
            info["now"]["feelsLike"],
            info['now']['windDir'],
            info['now']['windScale'],
            info['now']['windSpeed'],
            info['now']['humidity'],
            info['now']['pressure'],
            info['now']['vis']
        )
        return outcome
    except Exception as e:
        # print(e)
        return f"出错了! {city}没有天气信息！"

def get_city_id(city):
    try:
        rep = requests.get(f"https://geoapi.qweather.com/v2/city/lookup?location={city}&key={hefeng_key}").json()
        city_id = rep['location'][0]['id']
        return city_id
    except:
        return ''

def get_sun_info(city):
    city_id = get_city_id(city)
    if not city_id:
        return f'出错啦！未查到【{city}】！'

    today = gen_date().replace('-', '')

    url = 'https://devapi.qweather.com/v7/astronomy/sun?location={}&date={}&key={}'.format(
        city_id,
        today,
        hefeng_key
    )

    try:
        rep = requests.get(url).json()
        sunrise = rep['sunrise'].split('T')[-1].split('+')[0]
        sunset = rep['sunset'].split('T')[-1].split('+')[0]
        outcome = '{} {}\n🌅日出时间为{}\n🌄日落时间为{}!'.format(
            city,
            today,
            sunrise,
            sunset
        )
        return outcome
    except:
        return f'出错啦！'

def get_moon_info(city):
    city_id = get_city_id(city)
    if not city_id:
        return f'出错啦！未查到【{city}】！'
    
    today = gen_date().replace('-', '')

    url = 'https://devapi.qweather.com/v7/astronomy/moon?location={}&date={}&key={}'.format(
        city_id,
        today,
        hefeng_key
    )

    try:
        rep = requests.get(url).json()
        moonrise = rep['moonrise'].split('T')[-1].split('+')[0]
        moonset = rep['moonset'].split('T')[-1].split('+')[0]
        outcome = '{} {}\n🈷️出时间为{}\n🈷️落时间为{}!'.format(
            city,
            today,
            moonrise,
            moonset
        )
        return outcome
    except:
        return f'出错啦！'


if __name__ == '__main__':
    print(get_weather_info('青岛'))