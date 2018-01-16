#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RSSからXMLでランキングを取得しタグがitemのところだけをjsonで保存

"""
import sys
import codecs
import re,io
import urllib,urllib.request
import json
import datetime
from xml.etree.ElementTree import *
from collections import OrderedDict


today = datetime.datetime.today()
datename = today.strftime("%Y%m%d")

one_month = datetime.timedelta(days=1)



#url = "http://www.nicovideo.jp/ranking/view/daily/all?rss=2.0&page="
#dirpass = "daily_rank/"
url = "http://www.nicovideo.jp/ranking/view/monthly/all?rss=2.0&page="
dirpass = "monthly_rank/"




rank_id = []

#RnkingのURLからxml取得
for n in range(1,11):
    rank_url = url + str(n)
    req = urllib.request.Request(url=rank_url)
    fp = urllib.request.urlopen(req)
    rank_xml = fp.read().decode('utf-8')

    #windowsで表示する用
    #print(rank_xml.encode('cp932', "ignore").decode('cp932'))

    #XMLからすべてのitemを取得
    root = fromstring(rank_xml)
    link = root.findall(".//item/")


    #一つの動画データを辞書で保存し、それぞれの動画ごとのリストにする[動画１の辞書,動画2の辞書,...]
    rank_dict = OrderedDict()

    for e in link:
        if e.tag == 'title':
            #タイトルの先頭に来るランキング数字を新しい要素にする
            num = re.search('^第(\d*)位',e.text)
            rank_num = num.group(1)
            rank_dict.update({'rank':int(rank_num)})

            #タイトル前の「～位：」までを削除
            text = re.sub('^第(\d*)位：','',e.text)
            rank_dict.update({e.tag: text})
        elif e.tag == 'description':
            #descriptionを超えたら辞書をリストに入れる
            text = e.text
            rank_dict[e.tag] = text
            rank_id.append(rank_dict)
            rank_dict = OrderedDict()
        else:
            text = e.text
            rank_dict.update({e.tag: text})


today = datetime.datetime.today()
datename = today.strftime("%Y%m%d")

#辞書のリストをjsonで保存する
text = json.dumps(rank_id,indent = 4,ensure_ascii=False)
f = codecs.open(dirpass + datename + "_rank.json",'w','utf-8')
f.write(text)
