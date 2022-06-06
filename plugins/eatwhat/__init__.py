from command import register_cmd
from .dish import gen_random_dish


cmd = 'eatwhat'

def eatwhat_cmd(event):
    return '[CQ:at,qq={}]'.format(event.sender_id) + gen_random_dish()


register_cmd(cmd, eatwhat_cmd)