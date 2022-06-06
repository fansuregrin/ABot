from command import register_cmd
from config import port, address
import requests


cmd1 = 'muteme'
cmd2 = 'giveme'

def mute_cmd(event):
    duration_start = event.raw_msg.find('muteme') + len('muteme')
    raw_duration = event.raw_msg[duration_start::].strip()
    duration = raw_duration*60 if raw_duration.isdigit() else 60
    url = f"http://{address}:{port}/set_group_ban"
    params = {
        'group_id': event.group_id,
        'user_id': event.sender_id,
        'duration': duration
    }
    try:
        requests.get(url=url, params=params)
    except:
        pass

def giveme_cmd(event):
    spec_title_start = event.raw_msg.find('giveme') + len('giveme')
    spec_title = event.raw_msg[spec_title_start::].strip()
    url = f"http://{address}:{port}/set_group_special_title"
    params = {
        'group_id': event.group_id,
        'user_id': event.sender_id,
        'special_title': spec_title
    }
    try:
        requests.get(url=url, params=params)
        return '已给予{}<{}> 专属头衔: {}\n（可能不会生效，我也不知道为啥！）'.format(event.sender_name, event.sender_id, spec_title)
    except:
        pass


register_cmd(cmd1, mute_cmd)
register_cmd(cmd2, giveme_cmd)