from command import register_cmd
from .hefeng import get_weather_info, get_sun_info, get_moon_info


cmd = 'hf'

def tq_cmd(event):
    sub_cmd = event.get_sub_cmd(cmd)

    if not sub_cmd:
        outcome = '建议您使用hf help看看帮助手册'
        return outcome

    if sub_cmd == 'help':
        outcome = '''hf help 显示帮助手册
hf tq 查询城市天气
hf sun 查询城市日出日落'''
    elif sub_cmd == 'tq':
        city_start = event.raw_msg.find(sub_cmd) + len(sub_cmd)
        city = event.raw_msg[city_start::].strip()
        outcome = get_weather_info(city)
    elif sub_cmd == 'sun':
        city_start = event.raw_msg.find(sub_cmd) + len(sub_cmd)
        city = event.raw_msg[city_start::].strip()
        outcome = get_sun_info(city)
    elif sub_cmd == 'moon':
        city_start = event.raw_msg.find(sub_cmd) + len(sub_cmd)
        city = event.raw_msg[city_start::].strip()
        outcome = get_moon_info(city)
    else:
        outcome = f'[CQ:at,qq={event.sender_id}]暂无[{sub_cmd}]子命令!'

    return outcome


register_cmd(cmd, tq_cmd)