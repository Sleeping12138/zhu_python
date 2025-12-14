from pywinauto import Application

app = Application(backend='uia').connect(process=9624)

win = app.window(title='文件传输助手')
win.print_control_identifiers()

