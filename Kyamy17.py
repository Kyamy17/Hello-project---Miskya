import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from time import strftime
from tkcalendar import Calendar

todos = {}

def DetailTodo(cb = None):
    win = tk.Toplevel()
    win.wm_title("Detail Todo")
    tanggal = str(cal.selection_get)
    selecteditem = treev.focus()
    selectedIndex = treev.item(selecteditem)["text"]
    selectedTodo = todos[tanggal][selectedIndex]
    judul = tk.StringVar(value= selectedTodo["Titel/Title"])
    tk.Label(win, text = "Datum/Date:").grid(row = 0, column = 0, sticky = "N")
    tk.Label(win, text = "{} | {}".format(tanggal, selectedTodo["Zeit/Time"])).grid(row = 0, column = 1, sticky = "E")
    tk.Label(win, text = "Titel/Title:").grid(row = 1, column = 0, sticky = "N")
    tk.Entry(win, state = "disabled", textvariable = judul).grid(row = 1, column = 1, sticky = "E")
    tk.Label(win, text = "Information:").grid(row = 0, column = 2, sticky ="N")
    keterangan = ScrolledText(win, width = 12, height = 5)
    keterangan.grid(row = 2, column = 1, sticky = "E")
    keterangan.insert(tk.INSERT, selectedTodo["Information"])
    keterangan.configure(state = "disabled")

def LoadTodo():
    global todos
    f = open("mytodo.dat","r")
    data = f.read()
    f.close()
    todos = eval(data)
    ListTodo()


def SaveTodo():
    f = open("mytodo.dat","w")
    f.write(str(todos))
    f.close

def delTodo():
    tanggal = str(cal.selection_get())
    selecteditem = treev.focus()
    todos[tanggal].pop(treev.item(selecteditem)["text"])
    ListTodo()

def ListTodo(cb = None):
    for i in treev.get_children():
        treev.delete(i)
    tanggal = str(cal.selection_get())
    if tanggal in todos:
        for i in range(len(todos[tanggal])):
            treev.insert("","end", text = i, values = (todos[tanggal][i]["Zeit/Time"], todos[tanggal][i]["Titel/Title"]))

def addTodo(win, key, jam, menit, judul, keterangan):
    newTodo = {
        "Zeit/Time":"{}:{}".format(jam.get(), menit.get()),
        "Titel/Title": judul.get(),
        "Information": keterangan.get("1.0", tk.END)
    }
    if key in todos:
        todos[key].append(newTodo)
    else:
        todos[key] = [newTodo]
    win.destroy()
    ListTodo()


def addform():
    win = tk.Toplevel()
    win.wm_title("+")
    jam = tk.IntVar(value = 10)
    menit = tk.IntVar(value = 30)
    judul = tk.StringVar(value = "")
    tk.Label(win, text ="Zeit/Time:").grid(row = 0, column = 0)
    tk.Spinbox(win, from_ = 0, to = 23, textvariable = jam, width =3).grid(row = 0, column = 1)
    tk.Spinbox(win, from_ = 0, to = 59, textvariable = menit, width =3).grid(row = 0, column = 2)
    tk.Label(win, text= "Titel/Title:").grid(row = 1, column = 0)
    tk.Entry(win, textvariable = judul).grid(row = 1, column = 1, columnspan = 2)
    tk.Label(win, text = "Information:").grid(row = 2, column = 0)
    keterangan = ScrolledText(win, width = 12, height = 5)
    keterangan.grid(row = 2, column = 1, columnspan = 2, rowspan = 4)
    tanggal = str(cal.selection_get())
    tk.Button(win, text = "hinzugefügt/Add", command = lambda: addTodo(win, tanggal, jam, menit, judul, keterangan)).grid(row = 6, column = 0)

def title():
    waktu = strftime('%H:%H')
    tanggal = str(cal.selection_get())
    root.title(tanggal + "|" + waktu + " | My Calendar")
    root.after(1000, title)

root =tk.Tk()
s = ttk.Style()
s.configure("Treeview", rowheight = 16)
root.title("My Calendar")

cal = Calendar(root, font = "Forte 14", background='purple', bordercolor='purple', selectmode="day", locale="de_DE", cursor="star")
cal.grid(row=0, column=0, sticky="N", rowspan=7)
cal.bind("<<CalendarSelected>>", ListTodo)

tanggal = str(cal.selection_get())
treev = ttk.Treeview(root)
treev.grid(row=0, column=1, sticky="WNE", rowspan=4, columnspan=2)
scrollBar = tk.Scrollbar(root, orient="vertical", command = treev.yview)
scrollBar.grid(row=0, column=3, sticky="ENS", rowspan=4)
treev.configure(yscrollcommand = scrollBar.set)
treev.bind("<Double-1>", DetailTodo)
treev["column"] = ("1", "2")
treev["show"] = "headings"
treev.column("1", width = 100)
treev.heading("1", text = "Zeit/Time")
treev.heading ("2", text =  "Titel/Title")
 
btnadd = tk.Button(root, text = "hinzugefügt/Add", fg='white', background='purple', width = 30, command = addform)
btnadd.grid(row = 4, column = 1, sticky ="N")

btndel = tk.Button(root, text="Löschen/Delete", fg='white', background='purple', width = 30, command = delTodo)
btndel.grid(row = 4, column = 2, sticky = "N")

btnload = tk.Button(root, text = "Belastung/Load",fg='white', background='purple', width = 30, command = LoadTodo)
btnload.grid(row = 6, column = 1, sticky = "S")

btnsave = tk.Button(root, text ="Sparen/Save",fg='white', background='purple', width = 30, command = SaveTodo)
btnsave.grid(row = 6, column = 2, sticky = "S")
root.mainloop()