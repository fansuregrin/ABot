from command import register_cmd
from .fetch import get_bing_iotd


cmd = 'bitd'

def btd_cmd(event):
    try:
        return get_bing_iotd()
    except:
        return ''

register_cmd(cmd, btd_cmd)