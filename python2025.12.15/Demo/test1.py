import time

from pywinauto import Application, mouse

app = Application(backend='uia').connect(process=6180)

win = app.window(title_re=".*Sublime Text.*")
win.wait('ready')

# win.print_control_identifiers()

win.type_keys("hello world", with_spaces=True)

top_bar = win.child_window(title="应用程序", auto_id="MenuBar", control_type="MenuBar")

# top_bar.print_control_identifiers()

items = top_bar.items()

# for item in items:
#     point = item.rectangle().mid_point()
#     mouse.move(coords=(point.x, point.y))
#     time.sleep(1)


# open_recent = top_bar.item_by_path("File->Open Recent")
open_recent = win.menu_select("File -> Open Recent")
# open_recent.print_control_identifiers()
# print(open_recent.window_text())
