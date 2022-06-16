from bot_argparse import ArgumentParser
from command import register_cmd
from config import start_marks
from .moviedb import (
    search_multi,
    search_movie_proper,
    search_movie_implicit,
    search_tv_proper,
    search_tv_implicit
)


cmd = 'qtm'

def cmd_qtm(args):
    args = vars(args)
    parser = args['parser']
    if args['help']:
        return  '{}\n'\
                '用法: {} [-h] <s,m> ...\n'\
                '选项:\n'\
                ' -h, --help 获取帮助信息\n'\
                '子命令:\n'\
                's 通用搜索\n'\
                't 搜索电视剧\n'\
                'm 搜索电影'.format(
                    parser.description,
                    parser.prog
                )

def sub_cmd_s(args):
    args = vars(args)
    help_str = ('用法: qtm s [-h] [-p PAGE] [要搜索的内容]\n'
                '选项:\n'
                '-h, --help 获取帮助信息\n'
                '-p PAGE, --page PAGE  显示搜索结果的第几页，默认为第1页\n'
                '例如: qtm s 哈利波特 -p2')
    if args['help'] or not args['query']:
        return help_str
    query = args['query']
    page = args['page']
    return search_multi(query, page)

def sub_cmd_m(args):
    args = vars(args)
    
    parser = args['parser']
    if args['help'] or not args['query']:
        return  '用法: {} [-h] [-i] [-p PAGE] [要查询的电影]\n'\
                '选项:\n'\
                '-h, --help 获取帮助信息\n'\
                '-i, --implicit 开启模糊搜索\n'\
                '-p PAGE, --page PAGE  显示搜索结果的第几页\n'.format(
                    parser.prog
                )
    
    query = args['query']
    page = args['page']
    if args['implicit']:
        return search_movie_implicit(query, page)
    else:
        return search_movie_proper(query)

def sub_cmd_t(args):
    args = vars(args)
    
    parser = args['parser']
    if args['help'] or not args['query']:
        return  '用法: {} [-h] [-i] [-p PAGE] [要查询的电视剧]\n'\
                '选项:\n'\
                '-h, --help 获取帮助信息\n'\
                '-i, --implicit 开启模糊搜索\n'\
                '-p PAGE, --page PAGE  显示搜索结果的第几页\n'.format(
                    parser.prog
                )
    
    query = args['query']
    page = args['page']
    if args['implicit']:
        return search_tv_implicit(query, page)
    else:
        return search_tv_proper(query)


def qtm_parse_args(args):
    parser = ArgumentParser(prog=cmd, description='电影电视剧搜索程序', add_help=False)
    parser.add_argument('-h', '--help', action='store_true')
    parser.set_defaults(func=cmd_qtm, parser=parser)

    sub_parsers = parser.add_subparsers(title='子命令')

    parser_s = sub_parsers.add_parser('s', help='通用搜索', add_help=False)
    parser_s.add_argument('query', type=str, help='要搜索的内容', nargs='?', default='')
    parser_s.add_argument('-p', '--page', type=int, help='显示搜索结果的第几页', default=1, dest='page')
    parser_s.add_argument('-h', '--help', action='store_true')
    parser_s.set_defaults(func=sub_cmd_s, parser=parser_s)
    
    parser_m = sub_parsers.add_parser('m', help='搜索电影', add_help=False)
    parser_m.add_argument('query', type=str, help='要查询的电影', default='', nargs='?')
    parser_m.add_argument('-p', '--page', type=int, help='显示搜索结果的第几页', default=1, dest='page')
    parser_m.add_argument('-h', '--help', action='store_true')
    parser_m.add_argument('-i', '--implicit', action='store_true', help='开启模糊搜索', dest='implicit')
    parser_m.set_defaults(func=sub_cmd_m, parser=parser_m)

    parser_t = sub_parsers.add_parser('t', help='搜索电视剧', add_help=False)
    parser_t.add_argument('query', type=str, help='要查询的电视剧', default='', nargs='?')
    parser_t.add_argument('-p', '--page', type=int, help='显示搜索结果的第几页', default=1, dest='page')
    parser_t.add_argument('-h', '--help', action='store_true')
    parser_t.add_argument('-i', '--implicit', action='store_true', help='开启模糊搜索', dest='implicit')
    parser_t.set_defaults(func=sub_cmd_t, parser=parser_t)

    if not args:
        return '建议您使用"qtm --help"或"qtm -h"看看帮助手册，但别忘了以{}开头！'.format('或'.join(start_marks))
    try:
        args = parser.parse_args(args)
        if parser.error_info:
            return parser.error_info
        if parser_s.error_info:
            return parser_s.error_info
        if parser_m.error_info:
            return parser_m.error_info
        if parser_t.error_info:
            return parser_t.error_info
    except Exception as err:
        return str(err)
    
    return args.func(args)


def qtm_cmd(event):
    content_start = event.raw_msg.strip().find(cmd) + len(cmd)
    content = event.raw_msg[content_start::]
    outcome = '[CQ:at,qq={}]\n'.format(event.sender_id) + qtm_parse_args(content.split())

    return outcome


register_cmd(cmd, qtm_cmd)