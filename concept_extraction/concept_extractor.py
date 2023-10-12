import re

import dill
import MeCab
from crf_util import sent2features

# MeCabの初期化
mecab = MeCab.Tagger()
mecab.parse('')

# CRFモデルの読み込み
with open("crf.model", "rb") as f:
    crf = dill.load(f)


def extract_concept(utt):  # 発話文からコンセプトを抽出
    lis = []
    for line in mecab.parse(utt).splitlines():
        if line == "EOS":
            break
        else:
            word, feature_str = line.split("\t")
            features = feature_str.split(',')
            postag = features[0]
            lis.append([word, postag, "O"])

    words = [x[0] for x in lis]
    X = [sent2features(s) for s in [lis]]

    # 各単語に対応するラベル列
    labels = crf.predict(X)[0]

    # 単語列とラベル系列の対応を取って辞書に変換
    conceptdic = {}
    buf = ""
    last_label = ""
    for word, label in zip(words, labels):
        if re.search(r'^B-', label):
            if buf != "":
                _label = last_label.replace('B-', '').replace('I-', '')
                conceptdic[_label] = buf
            buf = word
        elif re.search(r'^I-', label):
            buf += word
        elif label == "O":
            if buf != "":
                _label = last_label.replace('B-', '').replace('I-', '')
                conceptdic[_label] = buf
                buf = ""
        last_label = label
    if buf != "":
        _label = last_label.replace('B-', '').replace('I-', '')
        conceptdic[_label] = buf

    return conceptdic


if __name__ == '__main__':
    for utt in ["お腹が痛いです", "下腹部が痛いんですよ", "頭の後ろがズキズキする", 'お腹が痛みます', 'お腹が痛む', 'お腹は痛くないです', 'お腹の下のほうが痛みます', "熱はないです",
                "下側です", "下のあたりです", "下の方が痛みます", "下側の方です"]:
        conceptdic = extract_concept(utt)
        print(utt, conceptdic)
