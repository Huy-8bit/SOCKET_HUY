from tkinter import *
import tkinter as tk
from tkinter import ttk
import socket
import json
from PIL import ImageTk, Image


def close():
    Client.sendto("exit".encode(FORMAT), ADDR)
    Client.close()
    window.quit()
    return


def handButton():
    data = ""
    data = txt.get()
    Client.sendto(data.encode(FORMAT), ADDR)

    if data == "exit":
        Client.sendto("exit".encode(FORMAT), ADDR)
        Client.close()
        return
    elif data == "list":
        temp = Client.recv(1024).decode(FORMAT)
        list = ""
        count = 1
        str = temp

        for item in str:
            if item == ',':
                count += 1
        for i in range(1, count + 1):
            # print(" " + str.split('"')[2*i - 1])
            list = list + str.split('"')[2*i - 1] + "\n"

        lbl.config(text="LIST dia diem: " + list, font=("Arial", 10))
        lbl.grid(row=0, column=0)
    elif data.split(' ')[0] == "check":
        temp = Client.recv(1024).decode(FORMAT)
        Client.sendto(data.encode(FORMAT), ADDR)
        temp1 = ""
        list = ""
        temp1 = Client.recv(1024)
        # print(temp1.decode(FORMAT))
        temp1 = temp1.decode(FORMAT)
        if temp1 == "false":
            list = "false"
        else:
            list = "Id: " + temp1.split('"')[3] + "\n" + "Ten dia diem: " + temp1.split('"')[7] + "\n" + "Toa do: " + temp1.split('"')[11]
        lbl.config(text="Ket qua check: " + list, font=("Arial", 10))
    elif data.split(' ')[0] == "image":
        Client.sendto(data.encode(FORMAT), ADDR)
        temp3 = ""
        # message check vietnam => temp = vietnam1.jpg
        temp3 = data.split(' ')[1] + "1.jpg"
        file_image = open(temp3, "wb")
        data_image = Client.recv(1024)
        if data_image == b"10101":
            print("File not found")
        else:
            while data_image != b"10101":
                file_image.write(data_image)  # file << data_image
                data_image = Client.recv(1024)
            file_image.close()
            lbl.config(text="File is downloaded", font=("Arial", 10))
            name_image = data.split(' ')[1] + "1.jpg"
            img = ImageTk.PhotoImage(Image.open(name_image))
            panel = Label(window, image=img)
            panel.grid(column=0, row=1)
            panel.image = img

    return


def handButtonCheck():
    data = "check "
    data = data + combo.get()
    
    Client.sendto(data.encode(FORMAT), ADDR)
    temp1 = ""
    list = ""
    temp1 = Client.recv(1024)
        # print(temp1.decode(FORMAT))
    temp1 = temp1.decode(FORMAT)
    if temp1 == "false":
        list = "false"
    else:
        list = "Id: " + temp1.split('"')[3] + "\n" + "Ten dia diem: " + temp1.split('"')[7] + "\n" + "Toa do: " + temp1.split('"')[11]
        lbl.config(text="Ket qua check: " + list, font=("Arial", 15), fg="BLUE")
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
window.geometry('500x500')
lbl = Label(window, text="APP", font=("Arial", 10), fg="red")
lbl.grid(column=0, row=0)
# # show image vietnam.jpg


txt = Entry(window, width=20, bg="white")
txt.grid(column=0, row=2)

btnHello = Button(window, text="Enter", command=handButton)
btnHello.grid(column=0, row=3)

btnClose = Button(window, text="Exit", command=close)
btnClose.grid(column=0, row=4)
Client.sendto("list".encode(FORMAT), ADDR)
temp = Client.recv(1024).decode(FORMAT)
list = []
count = 1
str = temp

for item in str:
    if item == ',':
        count += 1
for i in range(1, count + 1):
    # print(" " + str.split('"')[2*i - 1])
    list.append(str.split('"')[2*i - 1])


# combobox
textCombo = Label(window, text="Select a place: ")
textCombo.grid(column=0, row=5)
combo = ttk.Combobox(window, values=list)
combo.grid(column=0, row=6)

btnChoose = Button(window, text="Choose", command= handButtonCheck )
btnChoose.grid(column=0, row=7)

window.mainloop()




