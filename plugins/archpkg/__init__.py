from command import register_cmd
from .archpkg import *
from config import start_marks

cmd = 'arch'

def arch_cmd(event):
    raw_msg = event.raw_msg
    sub_cmd_start = raw_msg.strip().find(cmd) + len(cmd)
    raw_sub_cmd = raw_msg[sub_cmd_start::].strip().split(' ')[0]
    sub_cmd = raw_sub_cmd.lower()
    raw_msg = raw_msg.replace(raw_sub_cmd, sub_cmd, 1)
    args_start = raw_msg.find(sub_cmd) + len(sub_cmd)
    args = raw_msg[args_start::].strip().lower()

    outcome = None

    if sub_cmd == 'help':
        outcome = '''qrepo 查询官方仓库中的包
qaur 查询AUR中的包
srepo 搜索官方仓库中的包
saur 搜索AUR中的包
mrepo 查询官方仓库中包维护者
maur 查询AUR中包维护者'''
    elif sub_cmd == 'qrepo':
        outcome = get_pkg_info(args)
    elif sub_cmd == 'qaur':
        outcome = get_pkg_info_aur(args)
    elif sub_cmd == 'srepo':
        outcome = search_repo_pkg(args)
    elif sub_cmd == 'saur':
        outcome = search_aur_pkg(args)
    elif sub_cmd == 'mrepo':
        outcome = search_repo_maintainer(args)
    elif sub_cmd == 'maur':
        outcome = search_aur_maintainer(args)
    elif sub_cmd == '':
        outcome = '建议“arch help”看看帮助，不要忘记以“{}”开头！'.format('或'.join(start_marks))
    else:
        outcome = '无此子命令: [{}]'.format(sub_cmd)

    return outcome


register_cmd(cmd, arch_cmd)