from predefine import *

def listen(data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind(('', int(data['port'])))
    except socket.error as message:
        log('[r]Couldn\'t bind Elevate...@')
        log(f'[rD]Log: {message}@')
        sys.exit(1)
    s.listen(1)
    log('[n]Listenning...@')
    log(f'[nD]...on port {data["port"]}@')
    return s
    
def auth(s, data):
    # Authenticate secret
    secret = s.recv(40).decode()
    if secret[:4] != 'SECR':
        s.close()
        return False
    if secret[5:] == data['secret']:
        s.send('OK'.encode())
    else:
        s.send('NO'.encode())
        return False

    # Authenticate name
    name = s.recv(40).decode()
    if name[:4] != 'NAME':
        s.close()
        return False
    s.send('OK'.encode())
    return True

def recvFiles(s, data, newnames):
    buff = 4096
    path = os.path.join(data['path'], newnames["zip"])
    # Remove if already exists
    if os.path.exists(path):
        os.remove(path)
    file = open(path, 'wb')
    # Getting file's binary
    chunk = s.recv(buff)
    print('Soon')
    while True:
        file.write(chunk)
        chunk = s.recv(buff)
        if chunk.decode()[:9] == 'FILE:EXIT':
            break
    file.close()
    print('Got ya!')

def unboxProject(s, data, newnames):
    dir = os.path.join(data['path'], newnames['dir'])
    zip = os.path.join(data['path'], newnames['zip'])
    serverp = os.path.join(data['path'], newnames['dir'], newnames["server"])
    if os.path.exists(dir):
        code = os.system(f'rm -rf {dir}')
    code = os.system(f'unzip {zip} -d {dir}')
    if code:
        msg = 'Remote Elevate couldn\'t unzip the project'
        s.send(f'ERRR:{msg:<50}'.encode())
        return False
    try:
        result = process.check_output(['/bin/bash', serverp], stderr=process.STDOUT, timeout=60)
        status = ['OPEN', 'EXIT']
        s.send(f'BASH:{status[0]:<50}'.encode())
        # Buffer it somehow
        chunk = ''
        for char in result.decode():
            chunk += char
            if len(chunk) == 55:
                s.send(chunk.encode())
                chunk = ''
                
        s.send(f'{chunk:<55}'.encode())
        s.send(f'BASH:{status[1]:<50}'.encode())
    except:
        msg = 'Server script timed out'
        s.send(f'ERRR:{msg:<50}'.encode())
        return False
    return True


    # print(secret)
    # print()
    # if (secret[:5])
    # s.send(f'SECR:{config["secret"]}'.encode())
    # msg = s.recv(2).decode()
    # if msg == 'NO':
    #     log('[r]Remote Elevate rejected secret@')
    #     log('[rD]Your secret token is invalid@')
    #     sys.exit(-1)
    # elif msg == 'OK':
    #     log('[n]Remote Elevate recognized us 👋@')
    #     log('[nD]Your secret token is valid@\n')
    # else:
    #     log('[y]Couldn\'t understand remote Elevate@')
    #     log('[yD]Remote Elevate answered weird message@')
    #     log('[yD]It might be some kind of bug...@')
    #     log('[yD]You can try to restart both Elevate instances@')
    #     sys.exit(-1)
    
    # s.send(f'NAME:{data["name"]}'.encode())
    # s.recv(2).decode()
    # if msg == 'NO':
    #     log('[r]Remote Elevate rejected us by name@')
    #     log('[rD]Your name seems to not be on a whitelist@')
    #     sys.exit(-1)
    # if msg == 'OK':
    #     log('[n]Remote Elevate greeted us 🤝@')
    #     log('[nD]Your name is on a whitelist@\n')

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((socket.gethostname(), 3838))
# s.listen(1)

# buff = 1024

# while True:
#     client, address = s.accept()
#     print(f'connection from {address[0]}')
#     # Login procedure

#     file = open('illi.zip', 'wb')

#     while True:
#         chunk = client.recv(buff)
#         while chunk:
#             file.write(chunk)
#             chunk = client.recv(buff)
#         file.close()
#         break
#     client.close()
    

        
