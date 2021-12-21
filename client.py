import socket
import json
#from PIL import Image
HOST = "127.0.0.1"
PORT = 50001
ADDR = (HOST, PORT) # dia chi server
FORMAT = 'utf8'
message = ""
Client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print("Client is connected to server")
Client.sendto("Hello".encode(FORMAT), ADDR)
Client.recv(1024)
while True:
    data = input("Enter your message: ")
    if data == "exit":
        Client.sendto("exit".encode(FORMAT), ADDR)
        break
    elif data == "list":
        Client.sendto("list".encode(FORMAT), ADDR)
        temp = ""
        temp = Client.recv(1024).decode(FORMAT)
        count = 1
        str = temp
        for item in str:
            if item == ',':
                count += 1
        for i in range(1, count + 1):
            print(" " + str.split('"')[2*i - 1])
    
    elif data.split(' ')[0] == "image":
        Client.sendto(data.encode(FORMAT), ADDR)
        temp =""
        temp = data.split(' ')[1] + "1.jpg" # message check vietnam => temp = vietnam1.jpg
        file_image = open(temp, "wb")
        data_image = Client.recv(1024)
        if data_image == b"10101":
            print("File not found")
        else:
            while data_image != b"10101":
                file_image.write(data_image)  #file << data_image
                data_image = Client.recv(1024)
            file_image.close()
            print("File is downloaded")

        
    elif data.split(' ')[0] == "check":
        Client.sendto(data.encode(FORMAT), ADDR)
        temp1  = ""
        temp1 = Client.recv(1024)
        # print(temp1.decode(FORMAT))
        temp1 = temp1.decode(FORMAT)
        if temp1 == "false":
            print("Khong co du lieu")
        else:
            print("id: " + temp1.split('"')[3])
            print("ten dia diem: " + temp1.split('"')[7])
            print("toa do: " + temp1.split('"')[11])
    else:
        Client.sendto(data.encode(FORMAT), ADDR)
        message = Client.recv(1024).decode(FORMAT)
        print("Server" + message)
Client.close()
print("Client is disconnected from server")
input()