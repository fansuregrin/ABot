from command import register_cmd
from .translate import bd_trans

cmd = 'trans'


def trans_cmd(event):
    lang_type_start = event.raw_msg.find(cmd) + len(cmd)
    lang_type = event.raw_msg[lang_type_start::].strip().split()[0].strip()

    if lang_type == 'help':
        return '''trans [需要翻译成的语言] [翻译内容]
常用语言有:
中文 zh	英语 en
粤语 yue 文言文	wyw
日语 jp 韩语 kor
法语 fra 西班牙语 spa
泰语 th	阿拉伯语 ara
俄语 ru 葡萄牙语 pt	
德语 de	意大利语 it
希腊语 el 荷兰语 nl
波兰语 pl 保加利亚语 bul
爱沙尼亚语 est 丹麦语 dan
芬兰语 fin 捷克语 cs
罗马尼亚语 rom 斯洛文尼亚语 slo
瑞典语 swe 匈牙利语 hu
繁体中文 cht 越南语 vie'''

    content_start = event.raw_msg.find(lang_type) + len(lang_type)
    content = event.raw_msg[content_start::].strip()

    return bd_trans(content, lang_type)


register_cmd(cmd, trans_cmd)