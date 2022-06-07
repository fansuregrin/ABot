from config import nasa_api_key
from command import register_cmd
from .nasa import apod


cmd = 'nasa'


def nasa_cmd(event):
    sub_cmd = event.get_sub_cmd(cmd)

    if not sub_cmd:
        return f'建议您使用{cmd} help看看帮助手册'

    if sub_cmd == 'help':
        outcome = '''nasa help 显示帮助手册
nasa apod [YY-mm-dd] 获取NASA天文每日一图'''
    elif sub_cmd == 'apod':
        date_start = event.raw_msg.find(sub_cmd) + len(sub_cmd)
        date_ = event.raw_msg[date_start::].strip()

        if date_:
            outcome = apod(nasa_api_key, date_)
        else:
            outcome = apod(nasa_api_key)
    
    return outcome


register_cmd(cmd, nasa_cmd)