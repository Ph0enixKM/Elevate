from predefine import *

# def listen()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 3838))
s.listen(1)

buff = 1024

while True:
    client, address = s.accept()
    print(f'connection from {address[0]}')
    # Login procedure

    file = open('illi.zip', 'wb')

    while True:
        chunk = client.recv(buff)
        while chunk:
            file.write(chunk)
            chunk = client.recv(buff)
        file.close()
        break
    client.close()
    

        
