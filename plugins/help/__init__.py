from command import register_cmd


cmd = 'help'

def help_cmd(event):
    return """支持的命令有：
echo 回显
arch archlinux包查询等
bitd 发送必应每日一图
muteme 给自己冷静下
giveme 给我专属头衔，需带上头衔名称
hf 和风天气相关，可以使用hf help查看帮助
eatwhat 看看吃什么好
trans 翻译，需带上目标语言和翻译内容
qw 查英语单词
nasa NASA相关"""


register_cmd(cmd, help_cmd)