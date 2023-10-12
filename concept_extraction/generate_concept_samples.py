import random
import re
import xml.etree.ElementTree

import MeCab

from const import const


def random_generate(root):  # サンプル文に含まれる単語を置き換えることで学習用事例を作成
    buf = ""
    pos = 0
    posdic = {}
    # タグがない文章の場合は置き換えしないでそのまま返す
    if len(root) == 0:
        return root.text, posdic
    # タグで囲まれた箇所を同じ種類の単語で置き換える
    for elem in root:
        if elem.tag == "body":
            tmp = random.choice(const.body)
            buf += tmp
            posdic["body"] = (pos, pos + len(tmp))
            pos += len(tmp)
        elif elem.tag == "body_detail":
            tmp = random.choice(const.body_detail)
            buf += tmp
            posdic["body_detail"] = (pos, pos + len(tmp))
            pos += len(tmp)
        elif elem.tag == "parts":
            tmp = random.choice(const.parts)
            buf += tmp
            posdic["parts"] = (pos, pos + len(tmp))
            pos += len(tmp)
        elif elem.tag == "verb":
            tmp = random.choice(const.verb)
            buf += tmp
            posdic["verb"] = (pos, pos + len(tmp))
            pos += len(tmp)
        elif elem.tag == "noun":
            tmp = random.choice(const.noun)
            buf += tmp
            posdic["noun"] = (pos, pos + len(tmp))
            pos += len(tmp)
        if elem.tail is not None:
            buf += elem.tail
            pos += len(elem.tail)
    return buf, posdic

# 現在の文字位置に対応するタグをposdicから取得


def get_label(pos, posdic):
    for label, (start, end) in posdic.items():
        if start <= pos and pos < end:
            return label
    return "O"


# MeCabの初期化
mecab = MeCab.Tagger()
mecab.parse('')

# 学習用ファイルの書き出し先
fp = open("concept_samples.dat", "w")

da = ''
# eamples.txt ファイルの読み込み
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
            sample, posdic = random_generate(root)

            # lis は[単語，品詞，ラベル]のリスト
            lis = []
            pos = 0
            prev_label = ""
            for line in mecab.parse(sample).splitlines():
                if line == "EOS":
                    break
                else:
                    word, feature_str = line.split("\t")
                    features = feature_str.split(',')
                    # 形態素情報の0番目が品詞
                    postag = features[0]
                    # 現在の文字位置に対応するタグを取得
                    label = get_label(pos, posdic)
                    # label がOでなく，直前のラベルと同じであればラベルに'I-'をつける
                    if label == "O":
                        lis.append([word, postag, "O"])
                    elif label == prev_label:
                        lis.append([word, postag, "I-" + label])
                    else:
                        lis.append([word, postag, "B-" + label])
                    pos += len(word)
                    prev_label = label

            # 単語，品詞，ラベルを学習用ファイルに書き出す
            for word, postag, label in lis:
                fp.write(word + "\t" + postag + "\t" + label + "\n")
            fp.write("\n")

fp.close()
