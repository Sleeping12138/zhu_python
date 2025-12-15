import time

from pywinauto import Application

app = Application(backend='uia').connect(process=19956)

win = app.window(title_re='.*Sublime Text.*')
win.wait('visible')

# win.print_control_identifiers()

top_bar = win.child_window(title="应用程序", auto_id="MenuBar", control_type="MenuBar")

top_bar.print_control_identifiers()

print(top_bar.window_text())
print(top_bar.texts())

win.right_click_input()



# win.maximize()
# time.sleep(1)
#
# win.minimize()
# time.sleep(1)
#
# win.restore()