import requests
import os
import time
import re
from lxml import etree
from os import path
from config import images_dir


def get_bing_iotd():
    bing_pics = path.join(images_dir, 'bing_pics')
    today = time.strftime('%Y-%m-%d', time.localtime())
    
    url = 'http://cn.bing.com'
    resp = requests.get(url)
    tree = etree.HTML(resp.text)
    img_title = tree.xpath('/html/head/meta[@property="og:title"]/@content')[0]
    img_descp = tree.xpath('/html/head/meta[@property="og:description"]/@content')[0]
    img_url = tree.xpath('/html/head/link[@id="preloadBg"]/@href')[0]

    if not img_url.startswith('http'):
        img_url = url + img_url

    pattern = '.*?id=(.*?)&.*?'
    img_name = re.findall(pattern, img_url)[0]
    
    target_path = f'{bing_pics}/{img_name}'
    outcome = 'bing picture of today: {}\n标题: {}\n简介: {}...\n[CQ:image,file=bing_pics/{}]'.format(today, img_title, img_descp, img_name)

    if os.path.exists(target_path):
        return outcome
    
    img_bytes = requests.get(img_url).content
    if not path.exists(bing_pics):
        os.mkdir(bing_pics)
    if img_bytes:
        with open(target_path, 'wb') as fp:
            fp.write(img_bytes)
    
    return outcome


if __name__ == '__main__':
    get_bing_iotd()