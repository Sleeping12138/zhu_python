import time

from pywinauto import Application

app = Application(backend='uia').connect(process=22552)

win = app.window(title='计算器')

win.print_control_identifiers()
print(win.window_text())

clear_button = win.child_window(title="清除所有记忆", auto_id="ClearMemoryButton", control_type="Button")
clear_button.click_input()
time.sleep(1)

btn1 = win.child_window(title="一", auto_id="num1Button", control_type="Button")
btn1.click_input()
time.sleep(1)

add_btn = win.child_window(title="加", auto_id="plusButton", control_type="Button")
add_btn.click_input()
time.sleep(1)

btn2 = win.child_window(title="二", auto_id="num2Button", control_type="Button")
btn2.click_input()
time.sleep(1)

equal_btn = win.child_window(title="等于", auto_id="equalButton", control_type="Button")
equal_btn.click_input()
