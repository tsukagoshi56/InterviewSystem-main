
# from itertools import chain
import MeCab

tagger = MeCab.Tagger('-Owakati')
tagger.parse("")


class ConsoleBot:
    def __init__(self, system):
        self.system = system

    def start(self):
        """システムと対話をするための初期化を行う"""

        sessionId = "test_sessionId"
        return self.system.initial_message({'user_utt': None, 'sessionId': sessionId})

    def message(self, user_utt):
        """対話システムよりinputから発話を生成後、発話を出力

        Args:
            input_utt ([type]): ユーザからの発話
        """
        return self.system.reply({'user_utt': user_utt, 'sessionId': "myid"})

    def run(self, user_utt):
        """対話のフェーズにより関数を呼び出す

        対話開始時: self.start()
        ２回目以降: self.message()

        Args:
            user_utt (string): ユーザからの発話
        """

        if "/start" in user_utt:
            system_utt = self.start()
        else:
            system_utt = self.message(user_utt)

        if 'end' in system_utt['nextQ']:
            return {
                'sys_utt': system_utt['sys_utt'],
                'chat_ended': True
            }

        return {
            'sys_utt': system_utt['sys_utt'],
            'chat_ended': False
        }
