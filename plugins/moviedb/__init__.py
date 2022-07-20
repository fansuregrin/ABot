from ast import arg
from bot_argparse import ArgumentParser
from command import register_cmd
from config import start_marks
from .moviedb import (
    search_multi,
    search_movie_maybe,
    search_movie,
    fetch_movie,
    search_tv_maybe,
    search_tv,
    fetch_tv,
    search_person,
    trending
)


cmd = 'qtm'

def cmd_qtm(args):
    args = vars(args)
    parser = args['parser']
    if args['help']:
        return  '{}\n'\
                '用法: {} [-h] <s,m,t,d> ...\n'\
                '选项:\n'\
                ' -h, --help 获取帮助信息\n'\
                '子命令:\n'\
                's 聚合搜索\n'\
                't 搜索电视剧\n'\
                'm 搜索电影\n'\
                'd 热门趋势'.format(
                    parser.description,
                    parser.prog
                )

def sub_cmd_s(args):
    args = vars(args)
    help_str = ('用法: qtm s [-hmte] [-p PAGE] [-l LANG] <搜索内容>\n'
                '选项:\n'
                '-h, --help 获取帮助信息\n'
                '-m, --movie  指明搜索电影\n'
                '-t, --tv 指明搜索电视剧\n'
                '-e, --person 指明搜索人物\n'
                '-p PAGE, --page PAGE  显示搜索结果的第几页，默认为第1页\n'
                '-l LANG, --language LANG 结果返回的语言\n'
                '例如: qtm s 哈利波特 -p2 -m')
    if args['help'] or not args['query']:
        return help_str
    query = ' '.join(args['query'])
    page = args['page']
    language = args['language']
    if args['movie']:
        return search_movie(query, page, language)
    elif args['tv']:
        return search_tv(query, page, language)
    elif args['person']:
        return search_person(query, page, language)
    else:
        return search_multi(query, page, language)

def sub_cmd_m(args):
    args = vars(args)
    
    parser = args['parser']
    help_str = '用法: {} [-h] [-l LANG] [-i ID] <电影名>\n'\
                '选项:\n'\
                '-h, --help 获取帮助信息\n'\
                '-l LANG, --language LANG 指明结果返回的语言\n'\
                '-i ID, --id ID 指明电影id来查询\n'\
                '例如: qtm m 星际穿越'.format(
                    parser.prog
                )
    if args['help']:
        return help_str
    
    query = ' '.join(args['query']).strip()
    language = args['language']
    id = args['id']
    if id:
        return fetch_movie(id, language)
    elif query:
        return search_movie_maybe(query, language)
    else:
        return help_str

def sub_cmd_t(args):
    args = vars(args)
    
    parser = args['parser']
    help_str = '用法: {} [-h] [-i ID] [-l LANG] <剧集名>\n'\
                '选项:\n'\
                '-h, --help 获取帮助信息\n'\
                '-l LANG, --language LANG 指明结果返回的语言\n'\
                '-i ID, --id ID 指明电视剧id来查询\n'.format(
                parser.prog
                )
    
    if args['help']:
        return help_str
    
    query = ' '.join(args['query']).strip()
    language = args['language']
    id = args['id']
    if id:
        return fetch_tv(id, language)
    elif query:
        return search_tv_maybe(query, language)
    else:
        return help_str

def sub_cmd_d(args):
    args = vars(args)

    parser = args['parser']
    help_str = '用法: {} [-h] [-t TYPE] [-l LANG] [-w WINDOW]\n'\
                '选项:\n'\
                '-h, --help 获取帮助信息\n'\
                '-t, --type 类型: movie, tv, person, all\n'\
                '-l LANG, --language LANG 结果显示的语言\n'\
                '-w, --window 热门时间: day, week\n'.format(parser.prog)

    if args['help']:
        return help_str
    else:
        return trending(args['type'], args['window'], args['language'])


def qtm_parse_args(args):
    parser = ArgumentParser(prog=cmd, description='电影电视剧搜索程序', add_help=False)
    parser.add_argument('-h', '--help', action='store_true')
    parser.set_defaults(func=cmd_qtm, parser=parser)

    sub_parsers = parser.add_subparsers(title='子命令')

    parser_s = sub_parsers.add_parser('s', help='通用搜索', add_help=False)
    parser_s.add_argument('query', type=str, help='要搜索的内容', nargs='*')
    parser_s.add_argument('-p', '--page', type=int, help='显示搜索结果的第几页', default=1, dest='page')
    parser_s.add_argument('-l', '--language', type=str, help='结果返回的语言', default='zh', dest='language')
    parser_s.add_argument('-h', '--help', action='store_true')
    search_type_group = parser_s.add_mutually_exclusive_group()
    search_type_group.add_argument('-m', '--movie', action='store_true')
    search_type_group.add_argument('-t', '--tv', action='store_true')
    search_type_group.add_argument('-e', '--person', action='store_true')
    parser_s.set_defaults(func=sub_cmd_s, parser=parser_s)
    
    parser_m = sub_parsers.add_parser('m', help='搜索电影', add_help=False)
    parser_m.add_argument('query', type=str, help='要查询的电影名称', nargs='*')
    parser_m.add_argument('-i', '--id', type=int, default=0, dest='id')
    parser_m.add_argument('-l', '--language', type=str, default='zh', dest='language')
    parser_m.add_argument('-h', '--help', action='store_true')
    parser_m.set_defaults(func=sub_cmd_m, parser=parser_m)

    parser_t = sub_parsers.add_parser('t', help='搜索电视剧', add_help=False)
    parser_t.add_argument('query', type=str, help='要查询的电影名称', nargs='*')
    parser_t.add_argument('-i', '--id', type=int, default=0, dest='id')
    parser_t.add_argument('-l', '--language', type=str, default='zh', dest='language')
    parser_t.add_argument('-h', '--help', action='store_true')
    parser_t.set_defaults(func=sub_cmd_t, parser=parser_m)

    parser_d = sub_parsers.add_parser('d', help='趋势', add_help=False)
    parser_d.add_argument('-t', '--type', type=str, choices=['movie', 'tv', 'person', 'all'], default='all')
    parser_d.add_argument('-w', '--window', type=str, choices=['day', 'week'], default='day')
    parser_d.add_argument('-l', '--language', type=str, default='zh')
    parser_d.add_argument('-h', '--help', action='store_true')
    parser_d.set_defaults(func=sub_cmd_d, parser=parser_d)

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