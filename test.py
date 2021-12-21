from tkinter import *
import tkinter




window = Tk()
window.title("Welcome to LikeGeeks app")
window.geometry('350x200')
lbl = Label(window, text="Hello", fg="black", font=("Arial Bold", 50))
lbl.grid(column=0, row=0)


txt = Entry(window, width=10)
txt.grid(column=0, row=1)

def handButton():
    lbl.configure(text="NGH, " + txt.get())
    return

btnHello = Button(window, text="say hello", command=handButton)
btnHello.grid(column=1, row=1)


window.mainloop()
