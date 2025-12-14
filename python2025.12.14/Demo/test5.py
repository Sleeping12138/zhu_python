import time

from pywinauto import Application, mouse

app = Application(backend='uia').connect(process=26068)

win = app.window(title_re='.*Sublime Text.*')

# win.print_control_identifiers()

top_bar = win.child_window(title="应用程序", auto_id="MenuBar", control_type="MenuBar")

# top_bar.print_control_identifiers()

file_menu = top_bar.child_window(title="File", control_type="MenuItem")
file_menu.wait('visible')
file_menu.click_input()

point = file_menu.rectangle().mid_point()
mouse.move(coords=(point.x, point.y + 20))

# win.print_control_identifiers()

open_recent = win.child_window(title="Open Recent", control_type="MenuItem")
point = open_recent.rectangle().mid_point()
mouse.move(coords=(point.x, point.y))
time.sleep(2)

mouse.move(coords=(point.x + 400, point.y))

win.print_control_identifiers()

clear_items = top_bar.item_by_path("File -> Open Recent -> Reopen Closed File")
print(clear_items.texts())

# clear_items = win.child_window(title="Clear Items", auto_id="31", control_type="MenuItem")
# clear_items.click_input()

# win.print_control_identifiers()

# point = open_recent.rectangle().mid_point()
#
# mouse.move(coords=(point.x, point.y))
