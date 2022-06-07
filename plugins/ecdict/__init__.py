from command import register_cmd
from .stardict import StarDict
from config import ecdict_db_path


def query_word(event):
    dict = StarDict(ecdict_db_path)
    word_start = event.raw_msg.strip().find('qw') + len('qw')
    word = event.raw_msg[word_start::].strip()
    if not word:
        return '请带上要查询的单词！'
    
    word_obj = dict.query(word)
    
    if word_obj:
        exchange_map = {
            'p': '过去式',
            'd': '过去分词',
            'i': '现在分词',
            '3': '第三人称单数',
            'r': '形容词比较级',
            't': '形容词最高级',
            's': '名词复数形式',
        }
        if word_obj['exchange']:
            exchanges = word_obj['exchange'].split('/')
            exchanges_detail = ''
            for exchange in exchanges:
                exchanges_detail += f"{exchange_map[exchange.split(':')[0]]} -> {exchange.split(':')[1]}  "
        else:
            exchanges_detail = '无'
        
        outcome = '单词: {}\n音标: [{}]\n英文释义: {}\n中文释义: {}\n变体: {}'.format(
            word_obj['word'], 
            word_obj['phonetic'], 
            word_obj['definition'].replace('\\n', '\n'), 
            word_obj['translation'].replace('\\n', '\n'),
            exchanges_detail
        )
    else:
        outcome = '未查到[{}]!'.format(word)

    dict.close()

    return outcome


register_cmd('qw', query_word)