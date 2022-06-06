from config import nasa_api_key
from command import register_cmd
from .nasa import apod


def nasa_cmd(event):
    sub_cmd_start = event.raw_msg.find('nasa') + len('nasa')
    sub_cmd = event.raw_msg[sub_cmd_start::].strip().split()[0]

    if sub_cmd == 'apod':
        date_start = event.raw_msg.find(sub_cmd) + len(sub_cmd)
        date_ = event.raw_msg[date_start::].strip()

        if date_:
            return apod(nasa_api_key, date_)
        else:
            return apod(nasa_api_key)


register_cmd('nasa', nasa_cmd)