import csv

from elasticsearch import Elasticsearch, helpers

es = Elasticsearch()
SENARIO_COL = 4


def load():
    """[summary]
    .csvファイルから文章や状態番号をデータベースに登録
    index : 登録する質問データベース(大文字を入れてはいけない)
    query : ユーザ側の発話内容
    next_q : 次状態番号(この番号によって次の質問に遷移することができる)
    video_id : ビデオID(ユーザの回答によって変化し、何番のビデオを流すかを決める)
    sequence_id : シーケンスID(自由質問かYes/No質問かを0, 1で指定)
    Yields:
        [type]: [description]
    Yields:
        [type]: [description]
    """
    with open('senario_c.csv', 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        _ = next(reader)  # spik first row
        for row in reader:
            row_senario = row[:SENARIO_COL]
            if '' not in row_senario:
                print(row_senario)
                index = row_senario[0]
                query = row_senario[1]
                reaction = row_senario[2]
                next_q = row_senario[3]

                item = {'_index': str.lower(index),
                        '_type': 'docs',
                        '_source': {'query': query, 'reaction': str.lower(reaction), 'next_q': str.lower(next_q)}}

                yield item


if __name__ == "__main__":
    # timeoutエラーになる場合request_timeoutの値を大きくする(デフォルトは10)
    helpers.bulk(es, load(), request_timeout=30)
