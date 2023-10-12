import sys

import socketio  # https://python-socketio.readthedocs.io/en/latest/client.html

from console_bot_voice import ConsoleBot
from ebdm_system_c import EbdmSystem

# socketio クライアントを作る
socket_client = socketio.Client()

# engine client response event name (DO NOT CHANGE)
RESPONSE_EVENT = "engine_response"

# engine client response data structure
engine_client_response = {
    "command": "play_video",
    "video_id": 1,
    "sequence_id": 0,
    "chat_ended": False
}


@socket_client.event
def connect():
    print("サーバーに接続した。")
    socket_client.emit("join_room", "engine_app")
    # socket_client.emit(RESPONSE_EVENT, response_data)

# @socket_client.event
# def connect_error(data):
# 	print("接続失敗した、理由：", data)

# @socket_client.event
# def disconnect():
# 	print("接続切れました。")


""" engine側で対応するイベント """


@socket_client.event
def dialogue(data):
    engine_client_response = bot.run(data['text'])
    print(engine_client_response)

    while True:
        text = input('input something : ')
        engine_client_response = bot.run(text)
        socket_client.emit(RESPONSE_EVENT, engine_client_response)
        if engine_client_response["chat_ended"]:
            print("End of dialogue")
            sys.exit(0)


@socket_client.event
def human_detected(data):
    # dataを受け取ってresponse_data をここで準備。。。（あったら）
    # 。。。
    print('human detect')
    engine_client_response = bot.run('/start')
    socket_client.emit(RESPONSE_EVENT, engine_client_response)


@socket_client.event
def audio_message_obtained(data):
    # data["message"]の中にGoogleから受け取ったテキストが格納されている。
    # dataを受け取ってresponse_data をここで準備。

    print('USER:> ', data["message"])

    engine_client_response = bot.run(data["message"])
    socket_client.emit(RESPONSE_EVENT, engine_client_response)

    print("SYS:> ", engine_client_response['sys_utt'])

    if engine_client_response["chat_ended"]:
        # print("End of dialogue\n{}".format(utterances))
        print("End of dialogue")
        sys.exit(0)


@socket_client.event
def no_human_detected(data):
    # dataを受け取ってresponse_data をここで準備。（あったら）
    # 。。。
    pass


@socket_client.event
def age_gender_detected():
    # dataを受け取ってresponse_data をここで準備。（あったら）
    # 。。。
    # print("age_gender_detectedのイベントが届いた：{}".format(data))
    # socket_client.emit(RESPONSE_EVENT, response_data)
    pass


if __name__ == "__main__":
    SERVER_ADDRESS = 'http://192.168.1.154:5000'

    system = EbdmSystem()
    bot = ConsoleBot(system)

    socket_client.connect(SERVER_ADDRESS)
    socket_client.wait()
