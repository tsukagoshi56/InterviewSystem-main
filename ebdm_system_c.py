import csv
import random

import MeCab
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from console_bot_voice import ConsoleBot
from elasticsearch import Elasticsearch
from frame import FrameController

tagger = MeCab.Tagger('-Owakati')
tagger.parse("")


# 質問リストを読み込み
qlist = {}
with open('qlist_c.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    header = next(reader)  # 先頭行とばし
    for row in reader:
        # row[0]: q1_1
        # row[1]: こんにちは。今日お話を伺う対話システムです。よろしくお願いします。
        qlist[row[0].lower()] = row[1]

# リアクションリスト
reaction_list = ['そうですか。', 'なるほど。', 'わかりました。',
                 'はい、わかりました。', 'なるほど、そうですか。', 'そうですか、わかりました。', "", "", ""]


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
        self.fc = FrameController()

        self.currentQ = 'q1'
        self.repeat = False

    def initial_message(self, sessionId):
        """対話スタート時の固定発話

        Args:
            sessionId (string): セッションID(not used now)

        Returns:
            dict: システムの応答
        """
        return {
            'sys_utt': 'こんにちは。今日お話を伺う問診システムです。よろしくお願いします。本日はどうされましたか？',
            "nextQ": self.currentQ,
            'end': False
        }

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
        next_q = ''

        # 各方式共通
        # 相槌生成
        reaction_utt = random.choice(reaction_list)
        parrot_utt = ""
        question_utt = ""

        if self.currentQ in ['q1', 'q1_exp']:  # フレームを用いた状態遷移
            # 対話行為推定、コンセプト抽出、フレーム更新
            da, conceptdic = self.fc.da_concept.process(user_utt['user_utt'])
            frame, ok = self.fc.update(user_utt['user_utt'])
            print('da: {}, conceptdic: {}'.format(da, conceptdic))
            print(frame)
            if not ok:
                if not self.repeat:
                    self.repeat = True
                    utt = 'すみません、もう一度お伺いしてもよろしいですか？'

                else:
                    self.repeat = False

                    if self.currentQ == 'q1':
                        self.currentQ = 'q1_exp'
                        utt = "他に症状はありますか？"
                    elif self.currentQ == 'q1_exp':
                        self.currentQ = 'end_151'
                        utt = "心配でしたら病院に行って、診療を受けてください。"
                    else:
                        self.currentQ = 'q1_exp'
                        utt = "他に症状はありますか？"

                return {
                    'sys_utt': utt,
                    'nextQ': self.currentQ,
                    "end": False
                }

            self.repeat = False

            # オウム返し
            if da in ["body-symptoms-verb", "body-symptoms-noun", "body-symptoms-detail-verb", "body-symptoms-detail-noun", "other-symptoms"]:
                parrot_utt, max_score = self.query_parrot(
                    "parrot", frame['parrot_query'])
                if max_score < 0.4:  # cos類似度の最大値が規定値に満たない場合
                    parrot_utt = ""
                print('parrot_utt: {}, max_score: {}'.format(
                    parrot_utt, max_score))

            # 質問選択
            if frame['symptoms'] == "":
                question_utt = "そのほかの症状はありますか？"
            elif frame['body'] in ["おなか", "お腹", "腹", "はら", "腹痛"] and not frame['detailed']:
                question_utt = "具体的にどのあたりか分かりますか？"
            elif frame['fever'] == "":
                question_utt = "発熱はありますか？"
            else:  # ルールベースで最初に行う質問を検索
                next_q, max_score = self.query(
                    self.currentQ, frame['body'] + frame['symptoms'])

                if max_score < 0.1:  # cos類似度の最大値が規定値に満たない場合
                    self.currentQ = 'q1_exp'
                    return {'sys_utt': reaction_utt + '他に症状はありますか？', 'nextQ': self.currentQ, "end": False}
                if next_q == "q9":  # お腹の部位に関する質問
                    next_q, max_score = self.query(next_q, frame['body_parts'])
                if next_q in ["q3", "q5", "q10", "q15", "q19", "q26", "q27", "q34", "q39"]:  # 発熱に関する質問
                    next_q, max_score = self.query(next_q, frame['fever'])

                print('next_q: {}, question_utt: {}'.format(
                    next_q, question_utt))

                self.currentQ = next_q
                question_utt = qlist[next_q]

            print('self.currentQ: {}, question_utt: {}'.format(
                self.currentQ, question_utt))

            return {'sys_utt': reaction_utt + parrot_utt + question_utt, 'nextQ': self.currentQ, "end": False}

        else:  # ルールベース
            next_q, max_score = self.query(self.currentQ, user_utt['user_utt'])
            print('query: {} score: {}'.format(next_q, max_score))

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

                if next_q in ["q3", "q5", "q10", "q15", "q19", "q26", "q27", "q34", "q39"]:  # 発熱に関する質問
                    next_q, max_score = self.query(
                        next_q, self.fc.frame['fever'])

                    if max_score < 0.1:  # cos類似度の最大値が規定値に満たない場合
                        return {'sys_utt': reaction_utt + "もう一度お聞きしますが、" + qlist[self.currentQ], "nextQ": self.currentQ, "end": False}

                    self.currentQ = next_q

        return {'sys_utt': reaction_utt + qlist[self.currentQ], "nextQ": self.currentQ, "end": False}

    def query(self, index, user_utt):
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
        rep = self.__query(index, user_utt)
        for r in rep:
            score = self.evaluate(user_utt, r)
            # print('query: {}, user_utt: {}, score: {}'.format(str(r[0]), user_utt, str(score)))
            if score > max_score:
                max_score = score
                next_q = r[1]

        print('current: {}, next: {}'.format(index, next_q))

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

        results = self.es.search(index=question, query={
                                 'match': {'query': user_utt}}, size=100)
        return [
            (
                r['_source']['query'],
                r['_source']['next_q'],
            )
            for r in results['hits']['hits']
        ]

    def query_parrot(self, index, user_utt):
        """__query_parrotの結果から最も評価値が高いものを返す

        Args:
            user_utt (str): ユーザの入力内容

        Returns:
            next_q: 次の質問
            max_score: 最大の評価値
        """
        # cos類似度を比較
        parrot = ""
        max_score = -float('inf')  # 最も低い類似度スコア
        rep = self.__query_parrot(index, user_utt)
        for r in rep:
            score = self.evaluate(user_utt, r)
            # print('query: {} score: {}'.format(str(r[0]), str(score)))
            if score > max_score:
                max_score = score
                parrot = r[1]

        return parrot, max_score

    def __query_parrot(self, question, user_utt):
        """指定のElasticsearchインデックス(質問No.)から発話候補を探す

        Args:
            quesion (str): ユーザへの質問番号
            user_utt (str): ユーザの入力内容

        Returns:
            list: インデックスから検索した要素のリスト → [ユーザ発話推定文, 次状態]
        """
        results = self.es.search(index=question, query={
                                 'match': {'query': user_utt}}, size=100)
        return [
            (
                r['_source']['query'],
                r['_source']['reaction'],
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


if __name__ == '__main__':
    system = EbdmSystem()
    bot = ConsoleBot(system)

    sys_utt = bot.run('/start')
    print("SYS:> " + sys_utt['sys_utt'])

    while True:
        input_utt = input("YOU:> ")
        sys_utt = bot.run(input_utt)
        print("SYS:> " + sys_utt['sys_utt'])
