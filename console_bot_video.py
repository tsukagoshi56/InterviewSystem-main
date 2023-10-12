from sklearn.feature_extraction.text import CountVectorizer
import MeCab
import csv
from itertools import chain

tagger = MeCab.Tagger('-Owakati')
tagger.parse("")

Qlist  = []

# 質問リストと結果出力リストを.csvから読み込み
with open('qlist_a.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        row[0] = row[0].lower()
        Qlist.append(row)

class ConsoleBot:
    def __init__(self, system):
        self.system = system
 
    def start(self, input_utt):
        """[summary]
        辞書型 inputにユーザIDを設定
        システムからの最初の発話をinitial_messageから取得し,送信
        Args:
            input_utt ([type]): ユーザID
        Returns:
            str: 最初の発話を受け取った際のシステムの応答
        """
        input = {'utt': None, 'sessionId': "myid"}
        return self.system.initial_message(input)
 
    def message(self, input_utt):
        """[summary]
        辞書型 inputにユーザからの発話とユーザIDを設定
        replyメソッドによりinputから発話を生成後、発話を出力
        system_output["utt"] : インデックスで予め割り当てられたユーザの発言に対応する回答
        Qlist[int(system_output["currentQ"])] : 次の質問
        Args:
            input_utt ([type]): ユーザからの発話
        Returns:
            [type]: [description]
        """        
        input = {'utt': input_utt, 'sessionId': "myid"}
        system_output = self.system.reply(input)
        return system_output

    def run(self, text):
        """[summary]
        /startと入力されたら対話を開始する
        (クライアント側でhuman_detectedイベントが呼び出されたら入力するようになっている)
        状態遷移番号がendで対話終了フラグ(sys_out["end"])をTrueにし、対話終了
        """
        input_utt = text
        if "/start" in input_utt:
            sys_out = self.start(input_utt)

            response_data = {
                "command": "play_video",
                "video_id": 1,
                "sequence_id": 0,
                "chat_ended": False
            }

        else:
            sys_out = self.message(input_utt)
            pos = divmod(list(chain(*Qlist)).index(sys_out["currentQ"]), len(Qlist[0]))
            print("SYS : " + Qlist[pos[0]][1])

            response_data = {
                "command": "play_video",
                "video_id": sys_out["video_id"],
                "sequence_id": sys_out["sequence_id"],
                "chat_ended": sys_out["end"]
            }

            if sys_out["currentQ"] == 'end':
                response_data['chat_ended'] = True
                sys_out["end"] = True
                
        return response_data