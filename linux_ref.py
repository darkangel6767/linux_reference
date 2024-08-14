#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import simpledialog
from tkinter.messagebox import showinfo, showerror, askyesno
from pathlib import Path
import json

js_name = Path(__file__).stem + '.db'

def show_all():
    lst = []
    for key in db:
        lst.append(key)
    list1_items.set(value=lst)

def search(x, y, z):
    list1.selection_clear(0, END)
    text1.delete('1.0', END)
    buffer[0] = ''
    lst = []
    curval = edit1_value.get().lower()
    if curval.strip() == '':
        show_all()
        return
    for key, value in db.items():
        if curval in key.lower():
            lst.append(key)
    list1_items.set(value=lst)
    
def list_select(event):
    if len(list1.curselection()) == 0: return
    idx = list1.curselection()[0]
    last_selected[0] = idx
    key = list1.get(idx)
    text1.delete('1.0', END)
    text1.insert(END, db[key])
    buffer[0] = text1.get('1.0', END)

def list_add():
    q = simpledialog.askstring('Добавление записи', 'Заголовок:')
    if not q or q.strip() == '': return
    db[q] = ''
    edit1_value.set('')
    show_all()
    idx = list1_items.get().index(q)
    list1.select_clear(0, END)
    list1.select_set(idx)
    list1.see(idx)
    list1.event_generate('<<ListboxSelect>>')
    text1.focus()
    showinfo('Добавление записи', 'Успешно добавлено!')
    
def list_del():
    if len(list1.curselection()) == 0:
        showerror('Удаление записи', 'Сначала нужно выделить запись.')
        return
    idx = list1.curselection()[0]
    q = askyesno('Удаление записи', 'Удалить запись?')
    if q:
        item = list1.get(idx)
        del db[item]
        items = list(list1_items.get())
        items.remove(item)
        list1_items.set(value=items)
        showinfo('Удаление записи', 'Запись удалена!')

def list_edit():
    if len(list1.curselection()) == 0:
        showerror('Изменение заголовка', 'Сначала нужно выделить запись.')
        return
    idx = list1.curselection()[0]
    key = list1.get(idx)
    q = simpledialog.askstring('Редактирование заголовка', 'Новый заголовок:', initialvalue=key)
    if q and q != key:
        db[q] = db[key]
        del db[key]
        edit1_value.set('')
    
def text_cancel():
    text1.delete('1.0', END)
    text1.insert(END, buffer[0])
    
def text_clear():
    text1.delete('1.0', END)
    
def text_save():
    if len(list1.curselection()) == 0:
        showerror('Сохранение', 'Сначала нужно выделить запись для сохранения.')
        return
    idx = list1.curselection()[0]
    item = list1.get(idx)
    db[item] = text1.get('1.0', END).rstrip()
    showinfo('Сохранение', 'Запись сохранена!')

def text_select(event):
    try:
        text1.selection_get()
    except Exception:
        list1.selection_set(last_selected[0])

def edit_onfocus(event):
    if buffer[0] != '':
        buffer[0] = ''
    if text1.get('1.0', END) != '':
        text1.delete('1.0', END)

root = Tk()
root.title('Linux Reference Book')
edit1_value = StringVar()
edit1_value.trace('w', search)
list1_items = Variable(value=[])
frame1 = ttk.Frame(root)
label1 = Label(frame1, text='Поиск:')
edit1 = ttk.Entry(frame1, textvariable=edit1_value)
edit1.bind('<FocusIn>', edit_onfocus)
btn_add = Button(frame1, text='+', command=list_add)
btn_del = Button(frame1, text='-', command=list_del)
btn_edit = Button(frame1, text='\u270d', command=list_edit)
list1 = Listbox(root, listvariable=list1_items, selectmode=SINGLE)
list1.bind('<<ListboxSelect>>', list_select)
text1 = ScrolledText(root)
text1.bind('<<Selection>>', text_select)
frame2 = ttk.Frame(root)
btn_cancel = Button(frame2, text='Отмена', command=text_cancel)
btn_clear = Button(frame2, text='Очистить', command=text_clear)
btn_save = Button(frame2, text='Сохранить', command=text_save)
frame1.pack(pady=10)
label1.pack(side=LEFT, padx=10)
edit1.pack(side=LEFT, padx=10)
btn_add.pack(side=LEFT, padx=10)
btn_del.pack(side=LEFT, padx=10)
btn_edit.pack(side=LEFT, padx=10)
list1.pack(fill=X)
text1.pack(pady=5, fill=BOTH, expand=True)
frame2.pack(pady=50)
btn_cancel.pack(side=LEFT, padx=10)
btn_clear.pack(side=LEFT, padx=10)
btn_save.pack(side=LEFT, padx=10)
with open(js_name) as jf:
    db = json.load(jf)
buffer = ['']
last_selected = [0]
show_all()
root.mainloop()
with open(js_name, 'w') as jf:
    json.dump(db, jf)
