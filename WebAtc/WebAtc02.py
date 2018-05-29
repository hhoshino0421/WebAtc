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

# インポート定義
import urllib.request
import urllib.response
import queue
import threading
import os

# 定数定義
# スレッド数
threads = 10

# ターゲット
target = "http://www.nekonet.co.jp"
# 保存ディレクトリ
directory = "/home/hhoshino/temp"
# 除外するファイルの拡張子
filters = {".jpg", ".gif", ".png", ".css", ".jpeg"}

os.chdir(directory)

web_paths = queue.Queue()

for r, d, f in os.walk("."):
    for files in f:
        remote_path = "%s/%s" % (r,files)

        if remote_path.startswith("."):
            remote_path = remote_path[1:]

        if os.path.splitext(files)[1] not in filters:
            web_paths.put(remote_path)


def test_remote():
    while not web_paths.empty():
        path = web_paths.get()
        url = "%s%s" % (target, path)

    request = urllib.request(url)

    try:
        response = urllib.response(request)
        content = response.read()

        print("[%d] => %s" % (response.code, path))
        response.close()

    except:
        print("failed")
        pass


for i in range(threads):
    print("Spawning thread: %d" % i)
    t = threading.Thread(target=test_remote())
    t.start()