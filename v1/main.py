# from base64 import encode
# from pprint import pprint
# import time
import ctypes
import ctypes.wintypes
import win32gui
import win32con
import time
import re
import PySimpleGUI as sg
from layout import LayoutGUI
import datetime
from threading import Thread
import discordBOT

# from discordBOT import BOT
from User import User, UserData, LastPos
user = User()


def GetLocation(TargetWindowTitle: str):
    TargetWindowHandle = ctypes.windll.user32.FindWindowW(0, TargetWindowTitle)
    Rectangle = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(TargetWindowHandle, ctypes.pointer(Rectangle))
    return (Rectangle.left, Rectangle.top, )  # Rectangle.right, Rectangle.bottom)


def window_min(window_title: str = None):
    title = []

    def GetWindowTitle(hwnd):
        name = win32gui.GetWindowText(hwnd)
        if not re.match(".+CeVIO AI", str(name)) is None:
            title.append(name)

    if window_title is None:
        win32gui.EnumWindows(lambda hWnd, _: GetWindowTitle(hWnd), None)
    else:
        title.append(window_title)

    hwnd = win32gui.FindWindow(None, title[0])
    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)


def event_time():
    now = str(datetime.datetime.now().strftime("%Y/%m/%d %H:%m:%S : "))
    return now


class SubThread():
    def __init__(self):
        self.event_count = 0
        self.end_flg = False
        self.active_flg = False

    def start(self, contents):
        self.thread = Thread(
            target=self.loop_event,
            args=(contents,)
        )
        self.thread.start()

    def close(self):
        # discordBOT.end()
        if not self.active_flg:
            self.end_flg = True

        discordBOT.end()
        print(f"{event_time()}終了中ですしばらくお待ちください...")
        while True:
            if self.end_flg:
                break

    def loop_event(self, data):
        self.active_flg = True
        discordBOT.start(data)
        print(f"{event_time()}内部クリーンの為ソフトを終了します...")
        time.sleep(1.5)
        self.end_flg = True


def event_signup(username, pw1, pw2):
    if not pw1 == pw2:
        sg.popup(
            "パスワードが一致しません確認してください。",
            keep_on_top=True)
        return

    status = user.signup(username, pw1)

    if status == 1:
        sg.popup(
            "ユーザー登録に失敗しました",
            keep_on_top=True
        )
        return

    sg.popup(
        "正常に登録しました。",
        keep_on_top=True
    )
    return


def event_login(username, pw):
    data = user.login(username, pw)
    userdata = UserData(data, username, pw)
    if userdata.status == 1 or userdata.status == -1:
        sg.popup("ログインできませんでした。")
        return userdata

    return userdata


sg.theme("Dark")
window = LayoutGUI.make_login(LastPos().load_pos())
window_min()
st = SubThread()
ud = None

while True:
    window.keep_on_top_set()
    window.keep_on_top_clear()

    event, values = window.read()
    # print(window.__dict__)
    LastPos().save_pos(GetLocation(window.Title))
    print(f"イベント:{event}/値:{values}")

    if event == sg.WIN_CLOSED or event == "終了":
        st.close()
        break

    if event == "ログイン":
        username = values["-UserName-"]
        pw = values["-PassWord-"]
        status_obj = event_login(username, pw)

        if status_obj.status == 0:
            ud = status_obj
            location = GetLocation(window.Title)
            cast_list = discordBOT.get_casts()
            emotion_list = discordBOT.get_emotions(ud["cast"])
            window_main = LayoutGUI.make_setting(location, ud.datas,
                                                 cast_list, emotion_list)
            window.close()
            window = window_main
            print(f"{event_time()}ようこそユーザー樣")

    if event == "サインアップ":
        window_signup = LayoutGUI.make_signup()
        window.close()
        window = window_signup

    if event == "戻る":
        window_login = LayoutGUI.make_login()
        window.close()
        window = window_login

    if event == "登録":
        pw1 = values["-PassWord1-"]
        pw2 = values["-PassWord2-"]
        username = values["-UserName-"]
        event_signup(username, pw1, pw2)

    if event == "画面サイズ":
        print(window.size)
        print(GetLocation(window.Title))

    if event == "BOTを起動":
        if not st.active_flg:
            st.start(ud)
        else:
            sg.popup("BOTが起動中か、その他のエラーが発生しています")

    if event == "設定を反映する":
        for key in values:
            if not key == 0:
                ud.set_data(key, values[key])
                print(f"{key}を{values[key]}に書き換えました")
        discordBOT.change_data(values)

    if event == "コマンド接頭辞":
        message_text = "コマンドを呼び出す際の頭文字を指定してください。\n"
        message_text += "バグや、エラーを防ぐ為に特殊文字1文字が望ましいです。"
        prefix = sg.popup_get_text(
            message_text, title="command prefix?", default_text=ud["command_prefix"],
            keep_on_top=True
        )

        if prefix is not None:
            if not len(prefix) == 1:
                sg.popup("1文字ではありません操作をキャンセルします。")

            if len(prefix) == 1:
                print(prefix)
                ud.set_data("command_prefix", prefix)

    if event == "トークン":
        token_messeage = "DiscordのBOTに接続する為のトークン情報の入力してください。\n"
        token_messeage += "この情報は伏字で表示されます元に戻すことはできません。"

        distoken = sg.popup_get_text(
            token_messeage, title="discord token?", default_text=ud["token"],
            password_char="*", size=(60, 1), keep_on_top=True
        )

        print(ud["token"])
        if distoken is not None:
            ud.set_data("token", distoken)

    if event == "cast":
        cast = values["cast"]
        emotion_list = discordBOT.get_emotions("cast")
        window.FindElement("emotions").update(values=emotion_list)

    if event == "バージョン情報":
        sg.popup("version:1.0.0(a100)")

window.close()
