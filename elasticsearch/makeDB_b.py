import csv

from elasticsearch import Elasticsearch, helpers

es = Elasticsearch()

SENARIO_COL = 5


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
        _ = next(reader)
        for row in reader:
            row_senario = row[:SENARIO_COL]
            if '' not in row_senario:
                print(row_senario)
                index = row_senario[0]
                query = row_senario[1]
                next_q = row_senario[2]
                video_id = row_senario[3]
                sequence_id = row_senario[4]

                item = {'_index': str.lower(index),
                        '_type': 'docs',
                        '_source': {'query': query, 'next_q': str.lower(next_q), 'video_id': int(video_id), 'sequence_id': int(sequence_id)}}

                yield item


if __name__ == "__main__":
    # timeoutエラーになる場合request_timeoutの値を大きくする(デフォルトは10)
    helpers.bulk(es, load(), request_timeout=30)
