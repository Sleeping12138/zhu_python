from pywinauto import Application
from pywinauto.keyboard import send_keys

app = Application(backend='uia').connect(process=8640)

win = app.window(title='Untitled• - Typora')
win.wait('visible')

win.type_keys('hello   world', with_spaces=True)

win.type_keys('^s')