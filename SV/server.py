import socket
import json


def sendList(server, data_server, addr):
    list = []
    for item in data_server['data']:
        list.append(item['ten']) 
    
    server.sendto(json.dumps(list).encode(FORMAT), addr)
            

def sendDiadiem(server, data, addr, message):
    print("dia diem" , message)
    str =[]
    tempStr =""
    flag = False
    for item in data['data']:
        if item['ten'] == message:
            server.sendto(json.dumps(item).encode(FORMAT), addr)
            flag = True
            break
    if flag == False:
        server.sendto("false".encode(FORMAT), addr)

def sendImage(server, data, addr, message):
        print("run sendImage")
        flag = False
        for item in data['data']:
            if item['ten'] == message:    
                file_image = open(item['hinhAnh'], "rb") # open file in binary mode
                data_image = file_image.read(1024) # read file in 1024 bytes chunks
                while data_image: # send the file
                    server.sendto(data_image, addr)
                    data_image = file_image.read(1024) # read next chunk
                file_image.close()
                server.sendto(b"10101", addr)
                flag = True
                break
        if flag == False:
            server.sendto("false".encode(FORMAT), addr)

# 1024 1024 1024 1024


HOST = "127.0.0.1" # dia chi server
# SERVER_name = socket.gethostname()
# SERVER = socket.gethostbyname(SERVER_name)
global PORT
PORT = 50001
ADDR = (HOST, PORT) 
FORMAT = 'utf8'
server = socket.socket(socket.AF_INET, socket. SOCK_DGRAM)
server.bind(ADDR)  # tạo server tại ADDR này
data_server = []
with open("data.json", "r") as f:
    data_server = json.load(f)
flag = False
print("Server is running")
message, address = server.recvfrom(1024) # nhận message từ client, luu dia chi cua client vao address
print(message.decode(FORMAT)) # giai ma message va in ra
message = message.decode(FORMAT)  # cho quay ve kieu ky tu
server.sendto(message.encode(FORMAT), address)  # gửi lại cho client
while True:
    data, addr = server.recvfrom(1024) # nhận message từ client
    data = data.decode(FORMAT) # giai ma message va in ra
    
    if data == "exit": # nếu client gửi exit thì server sẽ thoát
        break
    print("server is connected from: ", addr)
    print("server is sending: ", data)
    if data == "list": 
        print("run sendList")
        sendList(server, data_server, addr)
    
    elif data.split(' ')[0] == "image":
         sendImage(server, data_server, addr, data.split(' ')[1])

    elif data.split(' ')[0] == "check":
        print("run checkDiadiem") 
        sendDiadiem(server, data_server, addr, data.split(' ')[1])
    
    else:        
        server.sendto("???".encode(FORMAT), addr)

server.close()
print("server is closed")
input()