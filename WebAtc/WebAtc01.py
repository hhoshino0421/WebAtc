"""
#
# urllibはPython3で変更された模様
# http://python-remrin.hatenadiary.jp/entry/2017/05/01/125011
#
# urllibはURLにアクセスするライブラリです。
# urllibモジュールは、Python 3 で urllib.request, urllib.parse, urllib.error に分割されて名称変更されました。
#
# ・urllib.request は URL を開いて読むためのモジュールです
# ・urllib.error は urllib.request が発生させる例外を持っています
# ・urllib.parse は URL をパース（構文解釈）するためのモジュールです
# ・urllib.robotparser は robots.txt ファイルをパースするためのモジュールです
#
"""

import urllib.request

url_str = "http://www.nekonet.co.jp/"

with urllib.request.urlopen(url_str
                         , data=None
                         , cafile=None
                         , capath=None
                         , cadefault=False
                         , context=None) as res:


    print("Code:" + str(res.getcode()))
    print("URL:" + res.geturl())
    #print("Info:" + res.info())
    print("")
    print("")

    print(res.read().decode('utf-8'))
