import socket # them vao thu vien socket
import json # import json
import os

def sendList(server, data_server, addr): # send list
    list = [] # list
    for item in data_server['data']: # vong lap cho tung item trong data
        list.append(item['ten']) # them item vao list
    
    server.sendto(json.dumps(list).encode(FORMAT), addr) # send list
            

def sendDiadiem(server, data, addr, message): # send diadiem
    print("dia diem" , message) # print message
    str =[] # str
    tempStr ="" # tempStr
    flag = False # flag
    for item in data['data']: # vong lap cho tung item trong data
        if item['ten'] == message: # neu ten cua item = message
            server.sendto(json.dumps(item).encode(FORMAT), addr) # send item
            flag = True # flag = true
            break # thoat vong lap
    if flag == False:# neu flag = false
        server.sendto("false".encode(FORMAT), addr) # send false

def sendImage(server, data, addr, message): # send image
        print("run sendImage") # in ra để báo hàm đã chạy
        flag = False # flag
        for item in data['data']: # vong lap cho tung item trong data
            if item['ten'] == message:    # neu ten cua item = message
                # kiem tra xem thu muc co ton tai khong
                if os.path.exists(item['hinhAnh']):
                    print("file ton tai")
                    file_image = open(item['hinhAnh'], "rb") # open file in binary mode 
                    data_image = file_image.read(1024) # read file in 1024 bytes chunks
                    while data_image: # send the file
                        flag = True # flag = true
                        server.sendto(data_image, addr) # send data_image
                        data_image = file_image.read(1024) # read next chunk
                    file_image.close() # close file
                    server.sendto(b"10101", addr) # send 10101 to client để thông báo rằng đã kết thúc file
                    break # thoat vong lap
                else: # neu khong ton tai
                    print("file khong ton tai")
                    server.sendto(b"false", addr) # send false

# 1024 1024 1024 1024


HOST = "127.0.0.1" # dia chi server
# SERVER_name = socket.gethostname()
# SERVER = socket.gethostbyname(SERVER_name)
global PORT # tao bien toan cuc
PORT = 50001 # port co gia tri 50001
ADDR = (HOST, PORT)  # dia chi server
FORMAT = 'utf8' # kieu du lieu gui di
server = socket.socket(socket.AF_INET, socket. SOCK_DGRAM) # tao socket
server.bind(ADDR)  # tạo server tại ADDR này
data_server = [] # tao mang data_server
with open("data.json", "r") as f: # mo file data.json
    data_server = json.load(f) # doc file data.json
flag = False # tao bien flag
print("Server is running") # in ra bao nhap server dang chay
message, address = server.recvfrom(1024) # nhận message từ client, luu dia chi cua client vao address
print(message.decode(FORMAT)) # giai ma message va in ra
message = message.decode(FORMAT)  # cho quay ve kieu ky tu
server.sendto(message.encode(FORMAT), address)  # gửi lại cho client
while True: # vong lap cho den khi client gui exit
    data, addr = server.recvfrom(1024) # nhận message từ client
    data = data.decode(FORMAT) # giai ma message va in ra
    
    if data == "exit": # nếu client gửi exit thì server sẽ thoát
        break # thoát
    print("server is connected from: ", addr) # in ra dia chi cua client
    print("server is sending: ", data) # in ra message cua client
    if data == "list": # nếu client yêu cầu list
        print("run sendList") # in ra để báo hàm đã chạy
        sendList(server, data_server, addr) # gọi hàm sendList
    
    elif data.split(' ')[0] == "image": # nếu client yêu cầu hình ảnh
         sendImage(server, data_server, addr, data.split(' ')[1]) # gọi hàm sendImage

    elif data.split(' ')[0] == "check": # nếu client yêu cầu check
        print("run checkDiadiem") # in ra để báo hàm đã chạy
        sendDiadiem(server, data_server, addr, data.split(' ')[1]) # gọi hàm sendDiadiem
    else:        
        server.sendto("???".encode(FORMAT), addr) # nếu không phải thì gửi lại cho client
 
server.close() # đóng server
print("server is closed") # in ra để báo server đã đóng
input() # đợi nhập vào để kết thúc