import requests
import os
import time
import re
from lxml import etree
from os import path
# from config import images_dir


images_dir = '/home/fansuregrin/.config/go-cqhttp/data/images'

def get_bing_iotd():
    bing_pics = path.join(images_dir, 'bing_pics')
    today = time.strftime('%Y-%m-%d', time.localtime())
    
    url = 'http://cn.bing.com'
    resp = requests.get(url)
    tree = etree.HTML(resp.text)
    img_title = tree.xpath('/html/head/meta[@property="og:title"]/@content')[0]
    img_descp = tree.xpath('/html/head/meta[@property="og:description"]/@content')[0]
    img_url = tree.xpath('/html/head/link[@id="preloadBg"]/@href')[0]

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

def bing_search():
    query = 'apple'
    url = 'https://cn.bing.com/search?q={}'.format(query)
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'cookie': 'MUID=084E7CD6D41E698F3F546D8AD56B6848; MUIDB=084E7CD6D41E698F3F546D8AD56B6848; _EDGE_V=1; SRCHD=AF=BDVEHC; SRCHUID=V=2&GUID=236667856D554F14BCC06C0031615DCA&dmnchg=1; NAP=V=1.9&E=1a4e&C=-1eVojLXq1Xsa-jYnv3f_D9U9YsPgq2LwH5YnBWO-x2or6-b4dhcfQ&W=1; BFBUSR=BAWAS=1&BAWFS=0; BFB=AhA7P7X_1kw7-I6YUda_zVVpHOuAGID41ymesfSDcLgnWTO1cJYudQR4yM3UHk-hc-rwBEppfHe44N4Vd0tl3stp7jexsc1BQGvyRh_ofV5_QAQ4DOAAVqcqLdc_jWJ6VZBo2YOdlgkkpP1ODA5zOACTZ9HFDPBaEz94S5O5z-cg0g; _UR=QS=0&TQS=0; _RwBf=ilt=1&ihpd=1&ispd=0&rc=0&rb=0&gb=0&rg=200&pc=0&mtu=0&rbb=0&g=0&cid=&clo=0&v=1&l=2022-05-30T07:00:00.0000000Z&lft=00010101&aof=0&o=2&p=&c=&t=0&s=0001-01-01T00:00:00.0000000+00:00&ts=2022-05-31T02:17:47.1517462+00:00&rwred=0; ZHCHATSTRONGATTRACT=TRUE; _EDGE_S=SID=37F458CEB41960A416994979B537610C; _SS=SID=37F458CEB41960A416994979B537610C; SRCHUSR=DOB=20220519&TPC=1654177216000; SNRHOP=I=&TS=; ipv6=hit=1654180817447&t=4; OID=AhCmKAa1Use2a0ITxs0zG9pXmx6plTIYk2atbyuaYkoEcG6grQhpQDUrujfpNaiwIXSPC9SFzveb3mK53XOY3UK7bJZNECUDiQVd26r5Gridhzocrs4hY_ouAOiKuzKR7j1H7dUdrXMFjTPumcWSc51v; OIDI=ghAiSlKqhhHOIYBQ8woSJoolKA9QMAhcussx8Y-W-dj4QXXbm4o5qiiDycik5OEqKyV5cI_PUBGc7kEaLdXLu74_M4W_YyI7hUgjfFQ5SAOHSC6OruHhK9P6wJ91-KECMg8Nyzs5anzHcPEwBTORV3AhaCJQwnEZ3O0nMOjPf29JhDY6ikNTntdtuWBFOHw3Fw00_9Z8A2dDfxzIDz6rc6InkXS0W1lML7qpfMqwmVFHs6pF5xdF4DEzj-jxdJAeCs-XKWcoYcPaJlam84_ffjPXETS2B-TuPph4fCyAAYcXcSd9LL6Ld45w0pWH2UHI47-AtD6TVerhGsYf1LYDXyOdq2PLAv_AbzcSiofPNCO5EX4vW80deLs0pILMffDMJVeZ6zsNf1pbyBNQ1BtpaU9sjkT7XFRvaiHJaxnA_5AOB4-Ye6ATiuhP1F7Kd53kwuqJZthjnvj3PowNgwTK9GzSLQOPxIL3CtqnMPOLCL_5RSl47Hd98pxsAMJbLHNjX5bVOgQmA9UxW7wbD5bYNdKV5D5u6Ml5npaDx0GmvHlTmTom4_iAMEeYrBCBWXdqGSR9RI4QKzJh9UTBHROP1Fa23aaV9PUvfgO40q-znKV-TNB7FPdvPwxQU25HabE1frSoB-7ECmiV4-sDt2TSD2J-qmAGRdxUCH56my0D7kUi7D_nYFoUil7Yy-_qoxKSANjprOFeJsUbt0RVJK-pBOo91ZY4QWxahJnPDNqGpi5chG5wPrzZNPyFhJuuuyleQCxva2Tap3eUwonsN7VyCqVpsKaRybJYZmVZsuRqsq4HcGleLpiZiJSnUKtgFLcscsRiHdv9DsSuDebr0ZFvn4PdoF8OlYzYQPy9oRcxeVjILZxTKlj0iN9YTckb90uHB_ZZYEI-hjK1tXH0rzu2pCijOnladte_ZeYDsEKwU6wVjrxL5GUGaDaz39v7VwWNLKyJbvETzSbS0wWvzZ9Q3B4-qQs3IRxtDt3FeMX4hamknI2xjJY3Om_-RlnZujnzzOCuR-qdabNDZCCF4oBQkacUfFDFK_x_Qe1ecRX-CyyGEcu6wqPHtEhJFifDSU3eZG6mnnInSP5NDuudPuGIICm63BIZyPU9C8K8EcCkw4Ap2qV4-yPcDneIz4XVWzGNphB_bin6hu6tDdY42MuCxwtqRtpLDd3DIPpXo1REuzmhh7hCpH2DptNoDsZ0Q0JaYFZl5FUGqbCLImCtScoPeIOuQsW6nNYD3k8grkbxW_fr64EGlE4k7fBgv5RYGYn4L8SQb_qV-7hAZgfAGreiRKCxZuWX5j5cen29V6qZvtoncrE_nr32738YYho20Tw5BGjVHDfez6vMvKI16B7UjdGEFI8NoKqDYHuvRGiEjR_DExWV8GZL2s9Gv15HlhTY3u476Y9Zw-cRq4_uJ8-Udo_wBX3kVnNC_Kfd7SA6lYXianCVtsZ5vl-RIVuOjjKzS3P2tYo9fB3_ujXUagz7OAUCWuYA3aY6x7ONZ5FEjXS9ABibpjnyVxvDEGGBOhX4tBXnmXOVqXcaw57yPay0TwxwaitJS9HfJsB6XoL6NgckqAPzRd8BmGiv6bRDM-Yhv16IzUrdX76MKBqSyeVkaYMhBkRE-JFaTzdv3APzonj93DihaglmN1tMwhMJ4-XLWonk9HHrUxbQdFVKmdUzJo652FAtmUcyyxlzWgOUaY6368pKyqb2VapIHuuD4HRNg09Qtoxvx1oDOBZqrmvFSiKisWwZIjlkL6R7YXqYiCycQaTY2iSpkCOYLBen_BRjFbmLVK13uu-wPWh63Kg0tniDPd1vIFozA-NReVz5OE7AIWLr-Vr2GTaCmjyPPk8bnGWBBDKxuCgVG9mADvzGPTPj_5bnvqSGcPLIcxfOhiO4ZooppmhKrDpLKV012evr_QYTYv-XzJRA5GIG13aW_7DC; OIDR=ghCCwC5RDW_QPqUheiX0cTSPLJnPCx6avqLaFpmpEhc0vAGSjTAHA83vS7XkAs1hTaXKIrdpPTapKtUkzZOXHA-K3VqVSav74Y4IVgvAy8naiHF5_fA5y72iDy0JW-ZWNcC1A4ECa5guPMeXdfnpLuEe16ltbyjivtIQuPswh_1gvCk3mVx_tCB9k_pwy8eGL-Y1pQqpeq612hSO-Tgiqx3B6x8Q0wZpT2cKBc4nfdmGff4gPRyPl2X9vjHb3JU9GvYIwVL5ExSbMzJTtRgsBeOov1ft7-Zuy9nPSGQ8nWhyL9msQO4b15aT16NH7vM9iAnTgVC2kpQ5S_eOEw1i_-LjnHoWTO3RhlNRta2EuR1LFjpiUy5FCAF_2osfQ2gsyGvlhSNO4f4ZOAUGjHEviXZvoZjO-QYUM_XYMPye7OqKwuBOK4IoGTOcJ3xlp-RcdJ5x4qtCRHL_loUBRz6EV9wgWB7nJtIWn67Q_ts67NV0rKWC6LJY1x8Gx0_cZNCHjCKIcbtmyXMbozw8p2LR80u7dvK-jy3Tzfx7o6luU0-Wb-ajuG7B8URT8hyEym44yUGGvIP_MDQ1_Z8kCrjHbwOmPsv5m-C210eZQtSzjf2afsl0XdHesVTKF5AbQ8lyIG3ofhkvPDkFthYByrgFRRN9tpRuuXhFlfWKDWHZex4QIcJdcVwASuyn5BDzLj2KA80JYOFq4OzibXWPDG105nazZjitRxiUbcAJsYtfPMAQ31sRwlkL3Oiobdd8to2o-IFxoqECcSJTsaFpUX6F3yn6JAEWevOBMwCl700lQEdy1LldvoWrVVAvtTrb2N0QgsLGJLhebgvfEGegfl9fQ1Tm9oKlDYLp2_EopGsM71Y7pFlLifuC8Df7N9ExkXhhzJsth4msLb_IFmwMsdVwRcPiQ9JgNgiT8E4Qjq2i4VyIBqyC1w6gDsMp9taZJsqEYLjGkMyMvD1qo3-5NZm6Fs4sJ-m835XVBw0KkUfzex7MsIbs8jTlxUud5m2f3XyxY32zUgNA4qLdiPCZCNvjJCHX; _HPVN=CS=eyJQbiI6eyJDbiI6NSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiUCJ9LCJTYyI6eyJDbiI6NSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiSCJ9LCJReiI6eyJDbiI6NSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyMi0wNi0wMlQwMDowMDowMFoiLCJJb3RkIjowLCJHd2IiOjAsIkRmdCI6bnVsbCwiTXZzIjowLCJGbHQiOjAsIkltcCI6MzZ9; ZHCHATWEAKATTRACT=TRUE; SRCHHPGUSR=SRCHLANG=en&PV=5.18.1&HV=1654177245&BRW=XW&BRH=S&CW=1905&CH=365&SW=1920&SH=1080&DPR=1&UTC=480&DM=0&BZA=0'
    }
    rep = requests.get(url=url, headers=headers).text
    print(rep)


if __name__ == '__main__':
    bing_search()