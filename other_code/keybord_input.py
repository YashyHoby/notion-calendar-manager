from pynput import keyboard

# キーの状態を追跡するための変数
r_pressed = False

def on_press(key):
    global r_pressed
    if key == keyboard.Key.esc:
        # プログラムを終了するためのキー
        return False
    try:
        if key.char == 'r' and not r_pressed:
            print('rキーが押されました')
            r_pressed = True
    except AttributeError:
        pass

def on_release(key):
    global r_pressed
    try:
        if key.char == 'r' and r_pressed:
            print('rキーが離されました')
            r_pressed = False
    except AttributeError:
        pass

# リスナーの登録
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
