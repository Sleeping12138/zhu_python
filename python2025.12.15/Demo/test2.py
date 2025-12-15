import time

from pywinauto import Application

app = Application(backend='uia').connect(process=6180)

win = app.window(title_re=".*Sublime Text.*")

win.maximize()

time.sleep(1)

win.restore()