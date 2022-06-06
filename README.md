# ABot

## Introduction
This is a simple chat robot for [tencent-qq](https://im.qq.com) based on [go-cqhttp](https://github.com/Mrs4s/go-cqhttp). The main function of this bot is to respond to commands sent by users in online chating room. Now, this bot supports the following commands.

- help: shows helpful manual to users.
- arch: about fetching information of packages on archlinux.
    - qrepo: query package's information from official repository of archlinux.
    - qaur: query package's information from Archlinux User Repository (AUR).
    - srepo: search package from official repository of archlinux.
    - saur: search package from Archlinux User Repository (AUR).
    - mrepo: fetch maintainer's information from official repository of archlinux.
    - maur: fetch maintainer's information from Archlinux User Repository (AUR).
    - help: show help manual.
- bitd: return a bing picture of today
- eatwhat: return a dish recommended to you.
- qw: query a English word.
- echo: echo what you say.
- hf: about hefeng weather
    - tq: fetch weather information of a city
    - sun: fetch information of sunrise and sunset of a certain city
    - moon: fetch information of moonrise and moonset of a certain city
- nasa: about nasa
    - apod: return a astronomy picture of the day. 
- muteme: let somebody in a group say nothing for a specific period(default 1 minute).
- giveme: give somebody a special-title in a group.
- trans: translate some sentences into target language.

## Installation
### Install go-cqhttp and cofig it
The most important thing you must notice is you should install [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) on your system. Then, you should config it well. This bot uses http protocal to communicate with go-cqhttp, so your go-cqhttp configuration maybe like this.

```yml
# go-cqhttp 默认配置文件

account: # 账号相关
  uin: 1234567890 # QQ账号
  password: '1234567890' # 密码为空时使用扫码登录
  encrypt: false  # 是否开启密码加密
  status: 10      # 在线状态 请参考 https://docs.go-cqhttp.org/guide/config.html#在线状态
  relogin: # 重连设置
    delay: 3   # 首次重连延迟, 单位秒
    interval: 3   # 重连间隔
    max-times: 0  # 最大重连次数, 0为无限制

  # 是否使用服务器下发的新地址进行重连
  # 注意, 此设置可能导致在海外服务器上连接情况更差
  use-sso-address: true

heartbeat:
  # 心跳频率, 单位秒
  # -1 为关闭心跳
  interval: -1

message:
  # 上报数据类型
  # 可选: string,array
  post-format: array
  # 是否忽略无效的CQ码, 如果为假将原样发送
  ignore-invalid-cqcode: false
  # 是否强制分片发送消息
  # 分片发送将会带来更快的速度
  # 但是兼容性会有些问题
  force-fragment: false
  # 是否将url分片发送
  fix-url: false
  # 下载图片等请求网络代理
  proxy-rewrite: ''
  # 是否上报自身消息
  report-self-message: false
  # 移除服务端的Reply附带的At
  remove-reply-at: false
  # 为Reply附加更多信息
  extra-reply-data: false
  # 跳过 Mime 扫描, 忽略错误数据
  skip-mime-scan: false

output:
  # 日志等级 trace,debug,info,warn,error
  log-level: warn
  # 日志时效 单位天. 超过这个时间之前的日志将会被自动删除. 设置为 0 表示永久保留.
  log-aging: 15
  # 是否在每次启动时强制创建全新的文件储存日志. 为 false 的情况下将会在上次启动时创建的日志文件续写
  log-force-new: true
  # 是否启用日志颜色
  log-colorful: true
  # 是否启用 DEBUG
  debug: false # 开启调试模式

# 默认中间件锚点
default-middlewares: &default
  # 访问密钥, 强烈推荐在公网的服务器设置
  access-token: ''
  # 事件过滤器文件目录
  filter: 'filter.json'
  # API限速设置
  # 该设置为全局生效
  # 原 cqhttp 虽然启用了 rate_limit 后缀, 但是基本没插件适配
  # 目前该限速设置为令牌桶算法, 请参考:
  # https://baike.baidu.com/item/%E4%BB%A4%E7%89%8C%E6%A1%B6%E7%AE%97%E6%B3%95/6597000?fr=aladdin
  rate-limit:
    enabled: false # 是否启用限速
    frequency: 1  # 令牌回复频率, 单位秒
    bucket: 1     # 令牌桶大小

database: # 数据库相关设置
  leveldb:
    # 是否启用内置leveldb数据库
    # 启用将会增加10-20MB的内存占用和一定的磁盘空间
    # 关闭将无法使用 撤回 回复 get_msg 等上下文相关功能
    enable: true

  # 媒体文件缓存， 删除此项则使用缓存文件(旧版行为)
  cache:
    image: data/image.db
    video: data/video.db

# 连接服务列表
servers:
  # 添加方式，同一连接方式可添加多个，具体配置说明请查看文档
  - http: # http 通信
      host: 127.0.0.1
      port: 8800
      timeout: 10 
      middlewares:
        <<: *default 
      post: 
      - url: http://127.0.0.1:8801
  #- ws:   # 正向 Websocket
  #- ws-reverse: # 反向 Websocket
  #- pprof: #性能分析服务器
  # 正向WS设置
  #- ws:
      # 正向WS服务器监听地址
      #host: 127.0.0.1
      # 正向WS服务器监听端口
      #port: 6700
      #middlewares:
      #  <<: *default # 引用默认中间件
  # 反向WS设置
  #- ws-reverse:
      # 反向WS Universal 地址
      # 注意 设置了此项地址后下面两项将会被忽略
      # universal: ws://127.0.0.1:8080/cqhttp/ws
      # 反向WS API 地址
      # api: ws://your_websocket_api.server
      # 反向WS Event 地址
      # event: ws://your_websocket_event.server
      # 重连间隔 单位毫秒
      # reconnect-interval: 3000
      # middlewares:
        #<<: *default # 引用默认中间件
```

### Run this bot
#### (1) Run through [`poetry`](https://python-poetry.org/)
Firstly, Downloads the source codes from this repository, and changes into the folder. Then, run `poetry init`.

Secondly, start this bot by typing `poetry run python3 main.py`.


#### (2) Run directly with python
Firstly, you should install some required dependencies. Downloads the source codes from this repository, and changes into the folder. Then, runs this following command.

```bash
pip install -r requirements.txt
```

Secondly, start this bot by typing the following command.

```
python3 main.py
```