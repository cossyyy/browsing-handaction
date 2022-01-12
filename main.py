import gui
import threading
from gesture_detection import gesture_detection
import time


#インスタンス化
object = gui.GUI()

def detection():
    while True:
        gesture_name = gesture_detection()

        if gesture_name == "thumbs up":
            object.scroll_up()

        elif gesture_name == "okay":
            object.scroll_down()

        elif gesture_name == "peace":
            object.page_back()

        elif gesture_name == "rock":
            object.page_forward()


thread = threading.Thread(target=object.start)

thread.start()

detection()




# #並行処理の設定
# thread = threading.Thread(target=operate)
# thread.start()

# object.start()

# thread.join()