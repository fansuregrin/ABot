from command import register_cmd


cmd = 'echo'

def echo_cmd(event):
    content_start = event.raw_msg.strip().find('echo') + len('echo')
    reply = event.raw_msg[content_start::]
    if len(reply) == 0:
        reply = '[CQ:at,qq={}]You SAY What???[CQ:face,id=0]'.format(event.sender_id)
    
    return reply


register_cmd(cmd, echo_cmd)