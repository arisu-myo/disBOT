import PySimpleGUI as sg
# def layout_setting():
#     default_button = ("Arial", 10)


class LayoutGUI:

    def soft_title():
        return "DisBOT(試用版)"

    def make_login(location=(None, None)):
        # left = 10
        # right = 10
        # top = 100
        # bottom = 100
        button_obj = [
            [
                sg.Button(
                    "ログイン",
                ),
                sg.Button(
                    "サインアップ"
                )
            ]
        ]

        layout = [
            [sg.Text("ログインしてください。")],
            [sg.Text("ユーザーネーム:", pad=((0, 0), (15, 0)))],
            [sg.Input(key="-UserName-")],
            [sg.Text("パスワード:", pad=((0, 0), (10, 0)))],
            [sg.Input(key="-PassWord-", password_char="●")],
            [sg.Column(button_obj, justification="right", pad=((0, 0), (10, 0)))],
            # [sg.Button("画面サイズ")]
        ]
        return sg.Window(
            LayoutGUI.soft_title(), layout, font=("Meiryo UI", 12), location=location,
            size=(380, 260), resizable=True, finalize=True)

    def make_signup():

        button_obj = [
            [
                sg.Button("登録"),
                sg.Button("戻る")
            ]
        ]

        layout = [
            [sg.Text("この画面はユーザーを登録する画面です")],
            [sg.Text("ユーザーネーム")],
            [sg.Input(key="-UserName-")],
            [sg.Text("パスワード")],
            [sg.Input(key="-PassWord1-", password_char="*")],
            [sg.Text("パスワード(確認)")],
            [sg.Input(key="-PassWord2-", password_char="*")],
            [sg.Column(
                button_obj,
                justification="right",
                pad=((0, 0), (10, 0))
            )]
        ]
        return sg.Window(
            LayoutGUI.soft_title(), layout, font=("Meiryo UI", 12),
            size=(300, 300), resizable=True, finalize=True)

    def make_main(location):
        layout = [
            [sg.Text("メインの画面のつもりです")],
            # [sg.Output(
            #     size=(100, 15),
            #     background_color="#000",
            #     text_color="#008000"
            # )],
            [
                sg.Button("終了"),
                sg.Button("BOTを起動"),
                sg.Button("設定")
            ]
        ]
        return sg.Window(
            LayoutGUI.soft_title(), layout, font=("Meiryo UI", 12), location=location,
            size=(640, 400), resizable=True, finalize=True
        )

    def make_setting(
        location=(None, None), datas: dict = None,
            cast_list: list = ["さとうささら"], emotion_list: list = ["普通"]):

        layout1 = [

            [sg.Text("キャスト:"),
                sg.Combo(cast_list, size=(20, 1), readonly=True,
                         default_value=datas["cast"], key="cast",)],

            [sg.Text("ボリューム:", pad=((0, 0), (20, 0))),
                sg.Slider((0, 100), orientation="h",
                          default_value=datas["volume"], key="volume")],

            [sg.Text("トーンスケール:", pad=((0, 0), (20, 0))),
                sg.Slider((0, 100), orientation="h",
                          default_value=datas["tonescale"], key="tonescale")],

            [sg.Text("スピード:", pad=((0, 0), (20, 0))),
                sg.Slider((0, 100), orientation="h",
                          default_value=datas["speed"], key="speed")],

            [sg.Text("感情:", pad=((0, 0), (20, 0))),
                sg.Combo(values=emotion_list, key="emotions", default_value=datas["emotions"],
                         size=(20, 1), pad=((0, 0), (20, 0)))],

            [sg.Text("感情値", pad=((0, 0), (20, 0))),
                sg.Slider((0, 100), orientation="h",
                          default_value=datas["emotions_value"], key="emotions_value")],

            [sg.Text("トーン", pad=((0, 0), (20, 0))),
                sg.Slider((0, 100), orientation="h",
                          default_value=datas["tone"], key="tone")],

            [sg.Text("アルファ", pad=((0, 0), (20, 0))),
                sg.Slider((0, 100), orientation="h",
                          default_value=datas["alpha"], key="alpha")],
        ]

        removes_message = "●写真など特殊な入力受け付けた場合の代替え文字です。\n"
        removes_message += "  デフォルトではブランク（空白）に設定されています。"

        file_message = "●通話に使用するファイルの場所、名前です。\n"
        file_message += "  名前には基本的に拡張子(.wav)を付けてください"

        layout2 = [
            [sg.Text(file_message, font=("Meiryo UI", 10), size=(50, 2),
                     background_color="#ffff00", text_color="#ff0000")],

            [sg.Text("保存場所:", pad=((0, 0), (0, 0))),
                sg.Input(key="file_paht", default_text=datas["file_path"],
                         size=(30, 1), pad=((0, 0), (0, 0)))],

            [sg.Text("ファイル名:", pad=((0, 0), (20, 20))),
                sg.Input(key="file_name", default_text=datas["file_name"],
                         size=(20, 1), pad=((0, 0), (20, 20)))],

            [sg.Text(removes_message, font=("Meiryo UI", 10), size=(50, 2),
                     background_color="#ffff00", text_color="#ff0000")],

            [sg.Text("絵文字:", pad=((0, 0), (0, 0))),
                sg.Input(key="remove_emoji", default_text=datas["remove_emoji"],
                         size=(20, 1), pad=((0, 0), (0, 0)))],

            [sg.Text("写真:", pad=((0, 0), (20, 0))),
                sg.Input(key="remove_picture", default_text=datas["remove_picture"],
                         size=(20, 1), pad=((0, 0), (20, 0)))],

            # [sg.Text("コマンド:", pad=((0, 0), (20, 0))),
            #     sg.Input(key="remove_command", default_text=datas["remove_command"],
            #              size=(20, 1), pad=((0, 0), (20, 0)))],

            [sg.Text("メインション:", pad=((0, 0), (20, 0))),
                sg.Input(key="remove_mention", default_text=datas["remove_mention"],
                         size=(20, 1), pad=((0, 0), (20, 0)))],

            [sg.Text("URL:", pad=((0, 0), (20, 0))),
                sg.Input(key="remove_url", default_text=datas["remove_url"],
                         size=(20, 1), pad=((0, 0), (20, 0)))],

        ]

        menu_layout = sg.MenuBar(
            [
                [
                    "ファイル(&F)",
                    [
                        "トークン",
                        "コマンド接頭辞",
                        "終了"
                    ]
                ],
                [
                    "情報(&I)",
                    [
                        "バージョン情報",
                        "ヘルプ（not found）"
                    ]
                ]
            ],
            background_color="#fff", text_color="#000", font=("Meiryo UI", "10")
        )

        buttonobj = [
            [
                sg.Button("設定を反映する"),
                sg.Button("終了"), sg.Button("BOTを起動"),
            ]
        ]
        # sg.Button("画面サイズ")

        main_layout = [
            [menu_layout],
            [sg.Text("⚙設定")],
            [
                sg.Frame("", layout1, size=(380, 400)),
                sg.Frame("", layout2, size=(400, 400)),
            ],
            [sg.Column(
                buttonobj,
                justification="right",
                pad=((0, 0), (10, 0))
            )]
        ]

        return sg.Window(
            LayoutGUI.soft_title(), main_layout, font=("Meiryo UI", 12), location=location,
            size=(820, 520), resizable=True, finalize=True
        )
