import MeCab
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from console_bot_video import ConsoleBot
from elasticsearch import Elasticsearch

tagger = MeCab.Tagger('-Owakati')
tagger.parse("")


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
        self.video_id = 1
        self.sequence_id = 0
        self.repeat = False

    def initial_message(self, input):
        """[summary]
        対話スタートと同時にシステム側で先に挨拶をする
        Args:
            input ([type]): 対話開始の際の入力文

        Returns:
            dict: システム側での応答文
        """
        self.currentQ = 'q1'
        self.video_id = 1
        self.sequence_id = 0
        self.repeat = False
        return {'utt': 'こんにちは、今日はどうされましたか？', 'end': False}

    def reply(self, user_utt):
        """[summary]
        max_score : 最も高い類似度スコア
        next_q : 次に遷移する質問番号
        video_id : 出力するビデオ番号
        sequence_id : 自由質問かYes/No質問かを0, 1で指定するシーケンス番号(現状全て0で設定している)
        計算したスコアに応じて応答文を選択し、出力
        どの発話にも当てはまらない場合(類似度が閾値を超えない場合)は別質問をする
        Yes / Noで答えられる質問で閾値を超えない場合(max_score < 0.1)は自己ループする
        Args:
            input (dict): Console上で入力された文章

        Returns:
            dict: Console上に出力する応答文
        """
        next_q, video_id, sequence_id, max_score = self.query(user_utt)

        # cos類似度の最大値が規定値に満たない場合
        if max_score < 0.1:
            if not self.repeat:
                self.repeat = True
                return {'currentQ': self.currentQ, "video_id": self.video_id, "sequence_id": self.sequence_id, "end": False}
            else:
                self.repeat = False

                if self.currentQ == 'q1':
                    self.currentQ = 'q1_exp'
                    self.video_id = 12
                elif self.currentQ == 'q1_exp':
                    self.currentQ = 'end'
                    self.video_id = 151
                else:
                    self.currentQ = 'q1_exp'
                    self.video_id = 12

        else:
            self.repeat = False
            self.currentQ = str.lower(next_q)
            self.video_id = video_id
            self.sequence_id = sequence_id

        return {"currentQ": self.currentQ, "video_id": self.video_id, "sequence_id": self.sequence_id, "end": False}

    def query(self, user_utt):
        """__queryの結果から最も評価値が高いものを返す

        Args:
            user_utt (str): ユーザの入力内容

        Returns:
            next_q: 次の質問
            max_score: 最大の評価値
        """
        max_score = -float('inf')
        rep = self.__query(user_utt['utt'])
        for r in rep:
            score = self.evaluate(user_utt['utt'], r[0])
            if score > max_score:
                max_score = score
                next_q = r[1]
                video_id = r[2]
                sequence_id = r[3]

        return next_q, video_id, sequence_id, max_score

    def __query(self, user_utt):
        """指定のElasticsearchインデックス(質問No.)から発話候補を探す

        Args:
            quesion (str): ユーザへの質問番号
            user_utt (str): ユーザの入力内容

        Returns:
            list: インデックスから引っ張ってきた要素のリスト → [推定文, 次状態, 動画ID, シーケンスID]
        """
        results = self.es.search(index=self.currentQ, body={
                                 'query': {'match': {'query': user_utt}}, 'size': 100, })
        return [
            (
                r['_source']['query'],
                r['_source']['next_q'],
                r['_source']['video_id'],
                r['_source']['sequence_id']
            ) for r in results['hits']['hits']
        ]

    def evaluate(self, user_utt, estimate_utt):
        """[summary]
        指定の評価基準に従って、最適な応答文を選択するための計算をする
        utt : ユーザ発話
        pair[0] : 用例ベースの発話
        pair[1] : 用例ベースの応答
        pair[2] : elasticsearchのスコア
        Args:
            utt ([type]): ユーザ発話
            pair ([type]): ペア文章

        Returns: 評価スコア
            [type]: [description]
        """
        return cosine(user_utt, estimate_utt)


if __name__ == '__main__':
    system = EbdmSystem()
    bot = ConsoleBot(system)

    response = bot.run('/start')
    print(response)
    while True:
        input_utt = input("YOU:>")

        if "/end" in input_utt:
            break

        response = bot.run(input_utt)
        print(response)
