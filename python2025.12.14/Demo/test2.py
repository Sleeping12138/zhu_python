from pywinauto import Application, mouse

app = Application(backend='uia').connect(process=22552)

win = app.window(title='计算器')

win.print_control_identifiers()

number_pad = win.child_window(title="数字键盘", auto_id="NumberPad", control_type="Group")

add_btn = win.child_window(title="加", auto_id="plusButton", control_type="Button")

clear_btn = win.child_window(title="清除所有记忆", auto_id="ClearMemoryButton", control_type="Button")

clear_btn.click_input()
print(number_pad.children())

for item in number_pad.children():
    point = item.rectangle().mid_point()
    mouse.click(coords=(point.x, point.y))
    add_btn.click_input()

result_btn = win.child_window(title="等于", auto_id="equalButton", control_type="Button")
result_btn.click_input()
