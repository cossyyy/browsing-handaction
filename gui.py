import tkinter as tk
from tkinter import ttk
from tkinter.constants import CENTER, E
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time


class GUI:

    def start(self):
        # ドライバーのインストール、起動
        self.browser = webdriver.Chrome(ChromeDriverManager().install())

        # 起動ボタンが押された時の処理
        def start_browser():
            # テキストボックスに書かれたurlの取得
            entry_text = txt_box.get()

            # 適切なurlに整形
            url = "https://" + entry_text

            # 指定されたurlへの移動
            time.sleep(1)
            self.browser.get(url)


        # ウィンドウの設定
        self.win = tk.Tk()
        self.win.geometry("300x200")
        self.win.title("python_gui")


        # メインフレームの作成と設置
        frame = tk.Frame(self.win)
        frame.pack(padx=20, pady=20)

        # ラベル
        label = ttk.Label(
            self.win,
            text="webページのurlを下に入力してください",
        )

        label.pack(anchor=tk.CENTER)


        # テキストボックス
        txt_box = ttk.Entry(
            self.win,
            width=20, 
            text="webページのurl"
        )

        txt_box.pack(pady=30, anchor=tk.CENTER)


        # ボタン
        button = ttk.Button(
            self.win,
            text="起動",
            command=start_browser,
        )

        button.pack(anchor=tk.CENTER)

        # guiの起動
        self.win.mainloop()


    # ウィンドウの消去
    def quit(self):
        self.win.destroy()

    
    """
    -------------------------------------------------------------------
    以下はブラウザの操作
    """

    # スクロールダウン
    def scroll_down(self):
        for x in range(1, 80, 5):
            scroll_down_script = "window.scrollBy(0, " + str(x) + ");"
            self.browser.execute_script(scroll_down_script)
            time.sleep(0.01)


    # スクロールアップ
    def scroll_up(self):
        for x in range(1, 80, 5):
            scroll_up_script = "window.scrollBy(0, " + str(-x) + ");"
            self.browser.execute_script(scroll_up_script)
            time.sleep(0.01)

    
    # 次のページへ
    def page_forward(self):
        self.browser.forward()

    
    # 前のページへ
    def page_back(self):
        self.browser.back()