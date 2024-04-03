import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import pysrt
import re

num_ENG = 1
num_CHN = 1

SRT_OUTPUT_PATH = ""
TXT_OUTPUT_PATH = ""

def replace_sub(srt, txt):
    subs = pysrt.open(srt)
    with open(txt, 'r', encoding='UTF-8') as f:
        txt_lines = f.readlines()
        txt_eng_lines = txt_lines[::2]
        txt_chn_lines = txt_lines[1::2]
    for i in range(len(subs)):
        subs[i].text = f'{txt_eng_lines[i]+txt_chn_lines[i]}'
    subs.save(SRT_OUTPUT_PATH, encoding='utf-8')

def open_file(txt):
    """Open a file for editing."""
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    txt.delete("1.0", tk.END)
    with open(filepath, mode="r", encoding="utf-8") as input_file:
        text = input_file.read()
        txt.insert(tk.END, text)
        add_highlight(txt, 1)
    window.title(f"双语字幕工作台1.0 - {filepath}")

def save_file(txt, save_path=False):
    """Save the current file as a new file."""
    filepath = asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
    )
    if not filepath:
        return
    with open(filepath, mode="w", encoding="utf-8") as output_file:
        text = txt.get("1.0", tk.END)
        output_file.write(text)
    window.title(f"Simple Text Editor - {filepath}")
    if save_path:
        global TXT_OUTPUT_PATH
        TXT_OUTPUT_PATH = filepath
        btn_combine["state"] = "normal"

def combine_subs():
    """combine saved txt_3 with the target .srt file"""    
    srt_filepath = askopenfilename(
        filetypes=[("Subtitle Files", "*.srt"), ("All Files", "*.*")]
    )
    if not srt_filepath:
        return
    global SRT_OUTPUT_PATH
    SRT_OUTPUT_PATH = srt_filepath
    replace_sub(srt_filepath, TXT_OUTPUT_PATH)

def add_highlight(txt, linenum):
    """add highlight to line"""
    txt.tag_add('highlightline', f'{linenum}.0', f'{linenum+1}.0')
    txt.tag_configure('highlightline', background='yellow')

def del_highlight(txt, linenum):
    """delete highlight"""
    txt.tag_remove("highlightline", f'{linenum}.0', f'{linenum+1}.0')

def open_popup():
    top= tk.Toplevel(window)
    top.geometry("500x200+500+300")
    #top.title("Reset current line number")
    top.title("重置当前处理行")
    tk.Label(top, text="新英文字幕行数:").place(x=20, y=40)
    tk.Label(top, text="新中文字幕行数:").place(x=20, y=60)
    eng_linenum = tk.StringVar()
    chn_linenum = tk.StringVar()
    tk.Entry(top,textvariable=eng_linenum).place(x=200, y=40)
    tk.Entry(top, textvariable=chn_linenum).place(x=200, y=60)
    #tk.Button(top, text="confirm", command=lambda:confirm_entry(eng_linenum.get(), chn_linenum.get())).place(x=50, y=100)
    tk.Button(top, text="确认", command=lambda:confirm_entry(eng_linenum.get(), chn_linenum.get())).place(x=50, y=100)
    #tk.Button(top, text="Cancel", command=lambda:cancel_entry(top))

def confirm_entry(eng_num, chn_num):
    global num_ENG, num_CHN
    del_highlight(txt_1, num_ENG)
    del_highlight(txt_2, num_CHN)
    num_ENG = int(eng_num)
    num_CHN = int(chn_num)
    add_highlight(txt_1, num_ENG)
    add_highlight(txt_2, num_CHN)
    

def cancel_entry(window):
    window.destroy()

def passed(txt1, txt2, txt3):
    global num_ENG, num_CHN
    line1 = txt1.get(f'{num_ENG}.0', f'{num_ENG}.end')
    line2 = txt2.get(f'{num_CHN}.0', f'{num_CHN}.end')
    txt3.insert(tk.END, line1+"\n"+line2+"\n")
    del_highlight(txt_1, num_ENG)
    del_highlight(txt_2, num_CHN)
    num_ENG+=1
    num_CHN+=1
    add_highlight(txt_1, num_ENG)
    add_highlight(txt_2, num_CHN)
    next_ENG = txt1.get(f'{num_ENG}.0', f'{num_ENG}.end')
    next_CHN = txt2.get(f'{num_CHN}.0', f'{num_CHN}.end')
    txt_4.delete("1.0", "2.1")
    txt_5.delete("1.0", "2.1")
    txt_4.insert(tk.END, next_ENG)
    txt_5.insert(tk.END, next_CHN)
    

def add(txt2, txt3):
    global num_CHN
    line = txt2.get(f'{num_CHN}.0',f'{num_CHN}.end')
    txt3.insert(tk.END, line+"\n")
    del_highlight(txt_2, num_CHN)
    num_CHN+=1
    add_highlight(txt_2, num_CHN)
    next_CHN = txt2.get(f'{num_CHN}.0', f'{num_CHN}.end')
    txt_5.delete("1.0", "2.1")
    txt_5.insert(tk.END, next_CHN)

def skip(txt1, txt3):
    global num_ENG
    line1 = txt1.get(f'{num_ENG}.0', f'{num_ENG}.end')
    txt3.insert(tk.END, line1+"\n\n")
    del_highlight(txt_1, num_ENG)
    num_ENG+=1
    add_highlight(txt_1, num_ENG)
    next_ENG = txt1.get(f'{num_ENG}.0', f'{num_ENG}.end')
    txt_4.delete("1.0", "2.1")
    txt_4.insert(tk.END, next_ENG)


window = tk.Tk()
window.title("双语字幕校对工具1.0")

#window.rowconfigure(1, minsize=300, weight=1)
#window.columnconfigure(0, minsize=300, weight=1)
#window.columnconfigure(1, minsize=300, weight=1)

# frame 1 (txt1, save1 & open1)
frame_1 = tk.Frame(window, relief=tk.RAISED, bd=2, width=400)
#frame_1.grid_propagate(False)

    
    # txt1
txt_1 = tk.Text(frame_1, width=60, height=50, wrap="none",  font=("Helvetica", 11))


    # button open&save file 1
#btn_open_1 = tk.Button(frame_1, text="Open", command=lambda:open_file(txt_1))
#btn_save_1 = tk.Button(frame_1, text="Save As...", command=lambda:save_file(txt_1))
btn_open_1 = tk.Button(frame_1, text="打开", command=lambda:open_file(txt_1))
btn_save_1 = tk.Button(frame_1, text="另存为...", command=lambda:save_file(txt_1))


# frame2 (txt2, save2 & open2)
frame_2 = tk.Frame(window, relief=tk.RAISED, bd=2)


    # txt2
txt_2 = tk.Text(frame_2, width=60, height=50, wrap="none",font=("Songti", 13))


    # button open&save file 2
#btn_open_2 = tk.Button(frame_2, text="Open", command=lambda:open_file(txt_2))
#btn_save_2 = tk.Button(frame_2, text="Save As...", command=lambda:save_file(txt_2))
btn_open_2 = tk.Button(frame_2, text="打开", command=lambda:open_file(txt_2))
btn_save_2 = tk.Button(frame_2, text="另存为...", command=lambda:save_file(txt_2))

# frame3 (txt3, pass, add next, done, skip)
frame_3 = tk.Frame(window, relief=tk.RAISED, bd=2)

txt_3 = tk.Text(frame_3, height=35, wrap="none", undo=True, font=("Helvetica", 11))
txt_4 = tk.Text(frame_3, height=2, wrap="none", font=("Helvetica", 11))
txt_5 = tk.Text(frame_3, height=2, wrap="none", font=("Helvetica", 11))

#btn_save_3 = tk.Button(frame_3, text="Save", command=lambda:save_file(txt_3, True))
#btn_combine = tk.Button(frame_3, text="Overwrite SRT", state="disabled", command=lambda:combine_subs())
btn_save_3 = tk.Button(frame_3, text="另存为...", command=lambda:save_file(txt_3, True))
btn_combine = tk.Button(frame_3, text="SRT插入", state="disabled", command=lambda:combine_subs())


#btn_pass = tk.Button(frame_3, text="Pass", height=5, command=lambda:passed(txt_1, txt_2, txt_3))
#btn_add = tk.Button(frame_3, text="Add", height=5, command=lambda:add(txt_2, txt_3))
#btn_done = tk.Button(frame_3, text="Reset", height=5, command=open_popup)
#btn_skip = tk.Button(frame_3, text="Skip", height=5, command=lambda:skip(txt_1, txt_3))
btn_pass = tk.Button(frame_3, text="合并", height=5, command=lambda:passed(txt_1, txt_2, txt_3))
btn_add = tk.Button(frame_3, text="添加中文行", height=5, command=lambda:add(txt_2, txt_3))
btn_done = tk.Button(frame_3, text="重置", height=5, command=open_popup)
btn_skip = tk.Button(frame_3, text="跳过英文行", height=5, command=lambda:skip(txt_1, txt_3))



frame_1.grid(row=0, column=0, sticky="ns")
frame_2.grid(row=0, column=2, sticky="ns")
frame_3.grid(row=0, column=4, sticky="ns")

btn_open_1.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save_1.grid(row=0, column=1, sticky="ew", padx=5)
txt_1.grid(row=1, column=0, columnspan=2, rowspan=4, sticky="nsew")

btn_open_2.grid(row=0, column=2, sticky="ew", padx=5, pady=5)
btn_save_2.grid(row=0, column=3, sticky="ew", padx=5)
txt_2.grid(row=1, column=2, columnspan=2, rowspan=4, sticky="nsew")

btn_save_3.grid(row=0, column=4, sticky="ew", padx=5, pady=5)
btn_combine.grid(row=0, column=5, sticky="ew", padx=5)
txt_3.grid(row=1, column=4, columnspan=2, rowspan=2, sticky="nsew")
txt_4.grid(row=3, column=4, columnspan=2, sticky="nsew")
txt_5.grid(row=4, column=4, columnspan=2, sticky="nsew")

btn_pass.grid(row=5, column=4, sticky="ew", padx=5, pady=5)
btn_skip.grid(row=5, column=5, sticky="ew", padx=5)
btn_add.grid(row=6, column=4, sticky="ew", padx=5)
btn_done.grid(row=6, column=5, sticky="ew", padx=5, pady=5)




window.mainloop()
