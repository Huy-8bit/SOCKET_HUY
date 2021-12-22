from tkinter import *
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import ttk
import socket
import json
from PIL import ImageTk, Image
import random


def close():
    Client.sendto("exit".encode(FORMAT), ADDR)
    Client.close()
    window.quit()
    return

def handButtonOpenImage(file_name):
    name_image = file_name + ".jpg"
    img = ImageTk.PhotoImage(Image.open(name_image))
    panel = Label(window, image=img, width=1280, height=720)
    panel.grid(column=0, row=1)
    # show panel with image
    panel.image = img
    # #zoom image
    btnCloseImage = Button(
        window, text="Close", command=lambda: panel.destroy() + btnCloseImage.destroy())
    btnCloseImage.grid(row=1, column=3)


def handButtonDownImage(name_image):
    data = "image " + name_image
    Client.sendto(data.encode(FORMAT), ADDR)
    temp3 = ""
    temp3 = data.split(' ')[1] + ".jpg"
    file_image = open(temp3, "wb")
    data_image = Client.recv(1024)
    if data_image == b"10101":
        print("File not found")
    else:
        while data_image != b"10101":
            file_image.write(data_image)  
            data_image = Client.recv(1024)
        file_image.close()
        lbl.config(text="File is downloaded", font=("Arial", 10))
        btnOpenImage = Button(window, text="OPEN", command=lambda: handButtonOpenImage(
            data.split(' ')[1]) + btnOpenImage.destroy())
        btnOpenImage.grid(row=0, column=0)
        btnOpenImage.place(relx=0.58, rely=0.15, anchor=CENTER)
    return


def handButtonCheck():
    data = "check "
    data = data + combo.get()
    Client.sendto(data.encode(FORMAT), ADDR)
    temp1 = ""
    list = ""
    temp1 = Client.recv(1024)
    temp1 = temp1.decode(FORMAT)
    if temp1 == "false":
        list = "false"
    else:
        list = "Id: " + temp1.split('"')[3] + "\n" + "Ten dia diem: " + temp1.split('"')[
            7] + "\n" + "Toa do: " + temp1.split('"')[11] + "\n" + "Mo ta: " + temp1.split('"')[15]

        handButtonDownImage(data.split(' ')[1])
    textDiaDiem = Label(window, text=list, font=("Arial", 25))
    textDiaDiem.grid(row=0, column=0)
    textDiaDiem.place(relx=0.5, rely=0.38, anchor=CENTER)
    
    # lbl.config(text="Ket qua check: " + list, font=("Arial", 15), fg="BLUE")

    
    return


HOST = "127.0.0.1"
PORT = 50001
ADDR = (HOST, PORT)  # dia chi server
FORMAT = 'utf8'
message = ""
Client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("Client is connected to server")
Client.sendto("Hello".encode(FORMAT), ADDR)
Client.recv(1024)

window = Tk()
window.title("Welcome to app made by Nguyen Gia Huy")
window.geometry('1350x730')

lbl = Label(window, text="APP", font=("Arial", 25), fg="red")
lbl.grid(column=0, row=0)
lbl.place(relx=0.5, rely=0.05, anchor=CENTER)


btnClose = Button(window, text="Exit", command=close)
btnClose.grid(column=0, row=0)
btnClose.place(relx=0.5, rely=0.25, anchor=CENTER)
Client.sendto("list".encode(FORMAT), ADDR)
temp = Client.recv(1024).decode(FORMAT)
list = []
count = 1
str = temp

for item in str:
    if item == ',':
        count += 1
for i in range(1, count + 1):
    list.append(str.split('"')[2*i - 1])


# combobox
textCombo = Label(window, text="Select a place: ", font=("Arial", 15))
textCombo.grid(column=0, row=0)
textCombo.place(relx=0.5, rely=0.1, anchor=CENTER)
combo = ttk.Combobox(window, values=list)
combo.grid(column=0, row=0)
combo.place(relx=0.5, rely=0.15, anchor=CENTER)
# btnChoose in center

btnChoose = Button(window, text="Choose", command=handButtonCheck, width=15)
btnChoose.grid(column=0, row=0)
btnChoose.place(relx=0.5, rely=0.2, anchor=CENTER)


window.mainloop()
