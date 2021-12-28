from tkinter import * 
import tkinter as tk  
from tkinter.filedialog import askopenfilename
from tkinter import ttk
import socket
import json
from PIL import ImageTk, Image
import random


def close(): # close window
    Client.sendto("exit".encode(FORMAT), ADDR) #gui thong diep exit 
    Client.close() #dong socket
    window.quit() #dong window
    return 

def handButtonOpenImage(file_name): # open image
    name_image = file_name + ".jpg" # ten file
    img = ImageTk.PhotoImage(Image.open(name_image)) # mo file
    panel = Label(window, image=img, width=1280, height=720) # tao label
    panel.grid(column=0, row=1) # dua label vao window
    # show panel with image
    panel.image = img # keep a reference
    # #zoom image
    btnCloseImage = Button( # tao nut close
        window, text="Close", command=lambda: panel.destroy() + btnCloseImage.destroy()) # tao nut close
    btnCloseImage.grid(row=1, column=3) # dua nut close vao window


def handButtonDownImage(name_image): # download image
    data = "image " + name_image # gui thong diep image
    Client.sendto(data.encode(FORMAT), ADDR) # gui thong diep image
    temp3 = "" # khoi tao chuoi temp3
    temp3 = data.split(' ')[1] + ".jpg" # lay ten file
    file_image = open(temp3, "wb") # mo file
    data_image = Client.recv(1024) # nhan data
    temp_message = data_image
    if temp_message == b"false": # nếu client không tồn tại file thì thông báo lỗi
        file_image.close() # dong file
        print("File not found")     
        lbl.config(text="File not found", font=("Arial", 25)) # thông báo lỗi
        return
    else: # nếu client tồn tại file thì ghi file
        while data_image != b"10101": # nếu data khác 10101 thì ghi file
            file_image.write(data_image)  # ghi file
            data_image = Client.recv(1024) # nhận data
        file_image.close() # đóng file
        lbl.config(text="File is downloaded", font=("Arial", 10)) # thông báo file đã được download
        btnOpenImage = Button(window, text="OPEN", command=lambda: handButtonOpenImage( # tao nut open
            data.split(' ')[1]) + btnOpenImage.destroy()) # tao nut open
        btnOpenImage.grid(row=0, column=0) # dua nut open vao window
        btnOpenImage.place(relx=0.58, rely=0.15, anchor=CENTER) # đặt vị trí
    return


def handButtonCheck(): # check file
    data = "check " # check file
    data = data + combo.get() # gui thong diep check
    Client.sendto(data.encode(FORMAT), ADDR) # gui thong diep check
    temp1 = "" # khoi tao chuoi temp1
    list = "" # khoi tao chuoi list
    temp1 = Client.recv(1024) # nhan data
    
    temp1 = temp1.decode(FORMAT) # decode data
    if temp1 == "false": # nếu client không tồn tại file thì thông báo lỗi
        list = "false" # gan list = false
    else: # nếu client tồn tại file thì ghi file
        list = "Id: " + temp1.split('"')[3] + "\n" + "Ten dia diem: " + temp1.split('"')[
            7] + "\n" + "Toa do: " + temp1.split('"')[11] + "\n" + "Mo ta: " + temp1.split('"')[15] # gan list = thong tin file

        handButtonDownImage(data.split(' ')[1]) # download file
    textDiaDiem = Label(window, text=list, font=("Arial", 25)) # tao label
    textDiaDiem.grid(row=0, column=0) # dua label vao window
    textDiaDiem.place(relx=0.5, rely=0.38, anchor=CENTER) # đặt vị trí vào giữa cửa sổ
    
    # lbl.config(text="Ket qua check: " + list, font=("Arial", 15), fg="BLUE")

    
    return


HOST = "127.0.0.1" # tạo địa chỉ máy chủ
PORT = 50001 # tạo cổng kết nối
ADDR = (HOST, PORT)  # dia chi server
FORMAT = 'utf8' # định dạng chuỗi
message = "" 
Client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # tạo socket
print("Client is connected to server") # in ra màn hình đã kết nối
Client.sendto("Hello".encode(FORMAT), ADDR) # gửi lời chào
# neu server khong mo thi thong bao
Client.recv(1024)

    

window = Tk() # tạo cửa sổ
window.title("Welcome to app socket") # đặt tiêu đề
window.geometry('1350x730') # đặt kích thước cửa sổ

lbl = Label(window, text="APP", font=("Arial", 25), fg="red") # tạo label đặt vào cửa sổ
lbl.grid(column=0, row=0) # đặt label vào cửa sổ
lbl.place(relx=0.5, rely=0.05, anchor=CENTER) # đặt label vào giữa cửa sổ


btnClose = Button(window, text="Exit", command=close) # tạo nút đóng
btnClose.grid(column=0, row=0) # đặt nút đóng vào cửa sổ
btnClose.place(relx=0.5, rely=0.25, anchor=CENTER) # đặt nút đóng vào giữa cửa sổ
Client.sendto("list".encode(FORMAT), ADDR) # gửi lệnh list để lấy danh sách dịch vụ
temp = Client.recv(1024).decode(FORMAT) # nhận danh sách dịch vụ
list = [] # tạo list
count = 1 # tạo biến đếm
str = temp # tạo chuỗi

for item in str: # duyệt danh sách dịch vụ
    if item == ',': # nếu gặp dấu ,
        count += 1 # tăng biến đếm
for i in range(1, count + 1): # duyệt danh sách dịch vụ
    list.append(str.split('"')[2*i - 1]) # thêm dịch vụ vào list


# combobox
textCombo = Label(window, text="Select a place: ", font=("Arial", 15)) # tạo label đặt vào cửa sổ
textCombo.grid(column=0, row=0) # đặt label vào cửa sổ
textCombo.place(relx=0.5, rely=0.1, anchor=CENTER) # đặt label vào giữa cửa sổ
combo = ttk.Combobox(window, values=list) # tạo combobox
combo.grid(column=0, row=0) # đặt combobox vào cửa sổ
combo.place(relx=0.5, rely=0.15, anchor=CENTER) # đặt combobox vào giữa cửa sổ
# btnChoose in center

btnChoose = Button(window, text="Choose", command=handButtonCheck, width=15) # tạo nút chọn
btnChoose.grid(column=0, row=0) #dặt nút chọn vào cửa sổ 
btnChoose.place(relx=0.5, rely=0.2, anchor=CENTER) # đặt nút chọn vào giữa cửa sổ


window.mainloop() # chạy cửa sổ lặp đi lặp lại
