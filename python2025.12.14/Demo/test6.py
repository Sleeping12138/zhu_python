import time

from pywinauto import Application

app = Application(backend='uia').connect(process=26068)

win = app.window(title_re='.*Sublime Text.*')

for i_file in range(5):
    win.type_keys(f"这是第 {i_file} 个文件")
    win.type_keys('^s')

    save_bar = win.child_window(title='另存为', control_type='Window')
    save_bar.wait("visible")

    file_name = f"D:\\testNote\\test{i_file}.txt"
    file_edit = save_bar.child_window(title="文件名:", auto_id="1001", control_type="Edit")
    file_edit.type_keys(file_name)

    save_btn = save_bar.child_window(title="保存(S)")
    save_btn.click_input()

    win.type_keys('^n')
