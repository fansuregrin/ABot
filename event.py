from utils import format_timestamp
from config import start_marks, commands, address, port, bot_name
import requests


base_url = f"http://{address}:{port}"


class Event(object):
    def __init__(self, post_data: dict):
        self.post_type = post_data['post_type']
        self.post_time = format_timestamp(post_data['time'])
        self.self_id = post_data['self_id']


class MetaEvent(Event):
    def __init__(self, post_data: dict):
        super().__init__(post_data)
        self.meta_event_type = post_data['meta_event_type']


class MessageEvent(Event):
    def __init__(self, post_data: dict):
        super().__init__(post_data)
        self.message_id = post_data['message_id']
        self.raw_msg = post_data['raw_message']
        self.sender_id = post_data['user_id']
        self.sender_name = post_data['sender']['nickname']
        self.msg_type = post_data['message_type']

    def triggle_command(self):
        for start_mark in start_marks:
            if self.raw_msg.strip().startswith(start_mark):
                raw_cmd = self.raw_msg.strip().lstrip(start_mark).strip().split(' ')[0]
                cmd = raw_cmd.lower()
                if cmd in commands.keys():
                    self.raw_msg = self.raw_msg.replace(raw_cmd, cmd, 1)
                    outcome = commands[cmd](self)
                else:
                    outcome = f"Sorry! [{cmd}] not found in my mind!"
                if outcome:
                    self.reply(outcome)
    
    def get_sub_cmd(self, cmd):
        sub_cmd_start = self.raw_msg.find(cmd) + len(cmd)
        try:
            sub_cmd = self.raw_msg[sub_cmd_start::].strip().split()[0]
        except:
            sub_cmd = ''

        return sub_cmd

    def reply(self, message):
        pass


class PrivateMessage(MessageEvent):
    def __init__(self, post_data: dict):
        super().__init__(post_data)
        self.sub_type = post_data['sub_type']
        self.temp_src = post_data['temp_source']
        self.__print_log__()

    def __print_log__(self):
        print("\033[1m->\033[0m [\033[34m{}\033[0m<\033[32m{}\033[0m> at (\033[31m{}\033[0m)]: {}".format(
            self.sender_name,
            self.sender_id, 
            self.post_time, 
            self.raw_msg))


class GroupMessageEvent(MessageEvent):
    def __init__(self, post_data: dict):
        super().__init__(post_data)
        self.group_id = post_data['group_id']
        self.sub_type = post_data['sub_type']
        self.is_anonymous = post_data['anonymous']
        self.__print_log__()
        self.triggle_command()

    def __print_log__(self):
        print("\033[1m->\033[0m [\033[34m{}\033[0m<\033[32m{}\033[0m> from group<\033[33m{}\033[0m> at (\033[31m{}\033[0m)]: {}".format(
            self.sender_name,
            self.sender_id,
            self.group_id, 
            self.post_time,
            self.raw_msg))

    def send_group_msg(self, message):
        url = base_url + '/send_group_msg'
        payload = {
            'group_id': self.group_id,
            'message': message,
            'auto_escape': 'false'
        }
        rsp = requests.get(url=url, params=payload).json()
        if rsp['status'] == 'ok':
            print('\033[1m<-\033[0m [\033[34m{}\033[0m<\033[32m{}\033[0m> send to group<\033[33m{}\033[0m>]: {}'.format(bot_name, 
            self.self_id, self.group_id, message))

    def reply(self, message):
       self.send_group_msg(message)


class NoticeEvent(Event):
    def __init__(self, post_data: dict):
        super().__init__(post_data)
        self.notice_type = post_data['notice_type']


class GroupMessageRecallEvent(NoticeEvent):
    def __init__(self, post_data: dict):
        super().__init__(post_data)
        self.group_id = post_data['group_id']
        self.sender_id = post_data['user_id']
        self.operator_id = post_data['operator_id']
        self.message_id = post_data['message_id']
        self.send_group_msg(self.__alert_recall__())

    def __alert_recall__(self):
        sender_nickname = self.__get_member_nickname__(self.sender_id)
        operator_nickname = self.__get_member_nickname__(self.operator_id)
        msg_recalled = self.get_msg(self.message_id)
        return ("{}<{}>\n撤回了\n{}<{}>\n在 {}发送的 【{}】!".format(
            operator_nickname,
            self.operator_id,
            sender_nickname,
            self.sender_id,
            self.post_time,
            msg_recalled
        ))

    def __get_member_nickname__(self, user_id):
        url = base_url + '/get_group_member_info'
        params = {
            'group_id': self.group_id,
            'user_id': user_id,
            'no_cache': 'false'
        }
        try:
            resp = requests.get(url=url, params=params).json()
            nickname = resp['data']['nickname']
            return nickname
        except Exception as err:
            # print(err)
            return ''

    def send_group_msg(self, message):
        url = base_url + '/send_group_msg'
        params = {
            'group_id': self.group_id,
            'message': message,
            'auto_escape': 'false'
        }
        rsp = requests.get(url=url, params=params).json()
        if rsp['status'] == 'ok':
            print('\033[1m<-\033[0m [\033[34m{}\033[0m<\033[32m{}\033[0m> send to group<\033[33m{}\033[0m>]: {}'.format(bot_name, 
            self.self_id, self.group_id, message))

    def get_msg(self, msg_id):
        url = f'{base_url}/get_msg?message_id={msg_id}'
        rsp = requests.get(url).json()
        outcome = ''
        if rsp['status'] == 'ok':
            msgs = rsp['data']['message']
            for msg in msgs:
                if msg['type'] == 'text':
                    outcome += msg['data']['text']
                elif msg['type'] == 'face':
                    outcome += f"[CQ:face,id={msg['data']['id']}]"
                elif msg['type'] == 'image':
                    outcome += f"[CQ:image,file={msg['data']['file']}]"
        else:
            outcome = '该消息不存在！'
        
        return outcome


def create_event(post_data: dict):
    event = None
    if post_data['post_type'] == 'meta_event':
        event = MetaEvent(post_data)
    elif post_data['post_type'] == 'message':
        if post_data['message_type'] == 'group':
            event = GroupMessageEvent(post_data)
        elif post_data['message_type'] == 'private':
            event = PrivateMessage(post_data)
    elif post_data['post_type'] == 'notice':
        if post_data['notice_type'] == 'group_recall':
            event = GroupMessageRecallEvent(post_data)

    return event