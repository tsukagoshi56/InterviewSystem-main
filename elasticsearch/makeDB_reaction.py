import csv

from const import const
from elasticsearch import Elasticsearch, helpers

es = Elasticsearch()
SENARIO_COL = 3


def load():
    """[summary]
    .csvファイルから文章や状態番号をデータベースに登録
    index : 登録する質問データベース(大文字を入れてはいけない)
    query : ユーザ側の発話内容
    next_q : 次状態番号(この番号によって次の質問に遷移することができる)
    video_id : ビデオID(ユーザの回答によって変化し、何番のビデオを流すかを決める)
    sequence_id : シーケンスID(自由質問かYes/No質問かを0, 1で指定)
    """
    with open("senario_c_parrot.csv", "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        _ = next(reader)  # skip first row
        for row in reader:
            row_senario = row[:SENARIO_COL]
            if "" not in row_senario:
                print(row_senario)
                index = row_senario[0]
                utterance = row_senario[1]
                parrot = row_senario[2]

                item = {"_index": str.lower(index),
                        "_type": "docs",
                        "_source": {"query": utterance, "reaction": parrot}}

                yield item


def createFile():
    with open("senario_c_parrot.csv", "w", encoding="utf-8-sig") as f:
        writer = csv.writer(f)

        header = ["index", "utterance", "reaction"]
        writer.writerow(header)

        for a in const.body_head:
            for b in const.parts:
                for c in const.verb + const.noun:
                    tmp = ["parrot"]
                    tmp.append(a + b + c)
                    tmp.append("頭の痛みですね？")
                    writer.writerow(tmp)
        for a in const.body_stomach:
            for b in const.parts:
                for c in const.verb + const.noun:
                    tmp = ["parrot"]
                    tmp.append(a + b + c)
                    tmp.append("お腹の痛みですね？")
                    writer.writerow(tmp)
        for a in const.body_chest:
            for b in const.parts:
                for c in const.verb + const.noun:
                    tmp = ["parrot"]
                    tmp.append(a + b + c)
                    tmp.append("胸の痛みですね？")
                    writer.writerow(tmp)
        for a in const.body_limbs:
            for b in const.parts:
                for c in const.verb + const.noun:
                    tmp = ["parrot"]
                    tmp.append(a + b + c)
                    tmp.append("手足の痺れですね？")
                    writer.writerow(tmp)
        for a in const.body_back:
            for b in const.parts:
                for c in const.verb + const.noun:
                    tmp = ["parrot"]
                    tmp.append(a + b + c)
                    tmp.append("背中の痛みですね？")
                    writer.writerow(tmp)
        for a in const.headache:
            tmp = ["parrot"]
            tmp.append(a)
            tmp.append("頭の痛みですね？")
            writer.writerow(tmp)
        for a in const.stomachache:
            tmp = ["parrot"]
            tmp.append(a)
            tmp.append("お腹の痛みですね？")
            writer.writerow(tmp)
        for a in const.breath:
            tmp = ["parrot"]
            tmp.append(a)
            tmp.append("呼吸についてですね？")
            writer.writerow(tmp)
        for a in const.cough:
            tmp = ["parrot"]
            tmp.append(a)
            tmp.append("咳についてですね？")
            writer.writerow(tmp)
        for a in const.heartburn:
            tmp = ["parrot"]
            tmp.append(a)
            tmp.append("胸焼けについてですね？")
            writer.writerow(tmp)


if __name__ == "__main__":
    createFile()

    # timeoutエラーになる場合request_timeoutの値を大きくする(デフォルトは10)
    helpers.bulk(es, load(), request_timeout=30)
