import random
import re
import xml.etree.ElementTree

from const import const


def random_generate(root):  # サンプル文に含まれる単語を置き換えることで学習用事例を作成
    buf = ""
    # タグがない文章の場合は置き換えしないでそのまま返す
    if len(root) == 0:
        return root.text
    # タグで囲まれた箇所を同じ種類の単語で置き換える
    for elem in root:
        if elem.tag == "body":
            tmp = random.choice(const.body)
            buf += tmp
        elif elem.tag == "body_detail":
            tmp = random.choice(const.body_detail)
            buf += tmp
        elif elem.tag == "parts":
            tmp = random.choice(const.parts)
            buf += tmp
        elif elem.tag == "verb":
            tmp = random.choice(const.verb)
            buf += tmp
        elif elem.tag == "noun":
            tmp = random.choice(const.noun)
            buf += tmp
        if elem.tail is not None:
            buf += elem.tail
    return buf


# 学習用ファイルの書き出し先
fp = open("da_samples.dat", "w")

da = ''
# examples.txt ファイルの読み込み
for line in open("../examples.xml", "r"):
    line = line.rstrip()
    # da= から始まる行から対話行為タイプを取得
    if re.search(r'^da=', line):
        da = line.replace('da=', '')
    # 空行は無視
    elif line == "":
        pass
    else:
        # タグの部分を取得するため，周囲にダミーのタグをつけて解析
        root = xml.etree.ElementTree.fromstring("<dummy>" + line + "</dummy>")
        # 各サンプル文を1000倍に増やす
        for i in range(1000):
            sample = random_generate(root)
            # 対話行為タイプ，発話文，タグとその文字位置を学習用ファイルに書き出す
            fp.write(da + "\t" + sample + "\n")

fp.close()
