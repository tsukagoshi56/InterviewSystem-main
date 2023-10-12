import csv

import MeCab
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from console_bot_voice import ConsoleBot
from elasticsearch import Elasticsearch

tagger = MeCab.Tagger('-Owakati')
tagger.parse("")


# 質問リストを読み込み
qlist = {}
with open('qlist_b.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    header = next(reader)  # 先頭行とばし
    for row in reader:
        # row[0]: q1_1
        # row[1]: こんにちは。今日お話を伺う対話システムです。よろしくお願いします。
        qlist[row[0].lower()] = row[1]


def cosine(a, b):
    """cos類似度の算出

    sklearnのvectorizerを使って単語頻度ベクトルを作り、cosine_similarityでcos類似度を計算する

    Args:
        a (str): 入力文1
        b (str): 入力文2

    Returns:
        float: 類似度スコア(高いほど2つの入力文は類似している)
    """

    a, b = CountVectorizer(
        token_pattern=u'(?u)\\b\\w+\\b').fit_transform([tagger.parse(a), tagger.parse(b)])
    return cosine_similarity(a, b)[0]


class EbdmSystem:
    def __init__(self):
        self.es = Elasticsearch()
        self.currentQ = 'q1'
        self.gender = 'unknown'
        self.repeat = False

    def initial_message(self, sessionId):
        """対話スタート時の固定発話

        Args:
            sessionId (string): セッションID(not used now) 

        Returns:
            dict: システムの応答
        """
        self.currentQ = 'q1'
        self.gender = 'unknown'
        self.repeat = False

        return {'sys_utt': 'こんにちは。今日お話を伺う対話システムです。よろしくお願いします。本日はどうされましたか？', 'nextQ': self.currentQ}

    def reply(self, user_utt):
        """ユーザ発話より次の質問をcos類似度で検索する

        どの発話にも当てはまらない場合(類似度が閾値を超えない場合)は別質問をする
        Yes / Noで答えられる質問で閾値を超えない場合(max_score < 0.1)は自己ループする

        Args:
            input (dict): Console上で入力された文章
                user_utt: ユーザの発話
                sessionId: セッションID(not used now)

        Returns:
            dict: システムの応答
        """
        next_q, max_score = self.query(user_utt)

        # print('query: {} score: {}'.format(str(next_q), str(max_score)))

        # cos類似度の最大値が規定値に満たない場合
        if max_score < 0.1:
            if not self.repeat:  # 必ず一度聞き返す
                self.repeat = True
                return {'sys_utt': 'すみません、よく聞こえませんでした。もう一度お伺いしてもよろしいですか？', 'nextQ': self.currentQ, "end": False}
            else:  # 二回目
                self.repeat = False

                if self.currentQ == 'q1':
                    self.currentQ = 'q1_exp'
                elif self.currentQ == 'q1_exp':
                    self.currentQ = 'end_151'
                else:
                    self.currentQ = 'q1_exp'

        else:
            self.repeat = False
            self.currentQ = next_q

        return {'sys_utt': qlist[self.currentQ], 'nextQ': self.currentQ, "end": False}

    def query(self, user_utt):
        """__queryの結果から最も評価値が高いものを返す

        Args:
            user_utt (str): ユーザの入力内容

        Returns:
            next_q: 次の質問
            max_score: 最大の評価値
        """
        # cos類似度を比較
        next_q = self.currentQ
        max_score = -float('inf')  # 最も低い類似度スコア
        rep = self.__query(self.currentQ, user_utt['user_utt'])
        for r in rep:
            score = self.evaluate(user_utt['user_utt'], r)
            # print('query: {} score: {}'.format(str(r[0]), str(score)))
            if score > max_score:
                max_score = score
                next_q = r[1]

        return next_q, max_score

    def __query(self, question, user_utt):
        """指定のElasticsearchインデックス(質問No.)から発話候補を探す

        Args:
            quesion (str): ユーザへの質問番号
            user_utt (str): ユーザの入力内容

        Returns:
            list: インデックスから検索した要素のリスト → [ユーザ発話推定文, 次状態]
        """
        # results['hits']['hits'] example
        # {'_index': 'q1_1', '_type': 'docs', '_id': 'im9h6IIBZjPDYhno5Eju', '_score': 0.8630463, '_source': {'query': 'よろしくお願いします。', 'reaction': 'お待たせしました。', 'next_q': 'q1_2'}}

        results = self.es.search(index=question, body={
                                 'query': {'match': {'query': user_utt}}, 'size': 100, })
        return [
            (
                r['_source']['query'],
                r['_source']['next_q'],
            )
            for r in results['hits']['hits']
        ]

    def evaluate(self, utt, pair):
        """指定の評価基準に従って、最適な応答文を選択するための計算をする

        Args:
            utt (str): ユーザ発話
            pair (str): ペア文章
                pair[0] : 用例ベースの発話
                pair[1] : 用例ベースの応答
                pair[2] : elasticsearchのスコア

        Returns: 評価スコア
            [type]: [description]
        """
        return cosine(utt, pair[0])

    # def interpret(self, utt):
    #     """発話を解釈し、必要なデータをシステム上に格納する

    #     Args:
    #         input (dict): Console上で入力された文章
    #             user_utt: ユーザの発話
    #             sessionId: セッションID(not used now)
    #     """
        # if self.currentQ == "q1_4":


if __name__ == '__main__':
    system = EbdmSystem()
    bot = ConsoleBot(system)

    sys_utt = bot.run('/start')
    print("SYS:> " + sys_utt['sys_utt'])

    while True:
        input_utt = input("YOU:> ")
        sys_utt = bot.run(input_utt)
        print("SYS:> " + sys_utt['sys_utt'])
