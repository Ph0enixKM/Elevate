from predefine import *

def connect(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, port))
        log('[n]Found Remote Elevate@')
        log('[nD]Connected to remote Elevate server@\n')
    except socket.error as message:
        log('[r]Elevate couldn\'t connect to the remote Elevate endpoint@')
        log(f'[rD]Log: {message}@')
    return s


def login(s, data):
    s.send(f'SECR:{data["secret"]}'.encode())
    msg = s.recv(2).decode()
    if msg == 'NO':
        log('[r]Remote Elevate rejected secret@')
        log('[rD]Your secret token is invalid@')
        exit(-1)
    elif msg == 'OK':
        log('[n]Remote Elevate recognized us 👋@')
        log('[nD]Your secret token is valid@\n')
    else:
        log('[y]Couldn\'t understand remote Elevate@')
        log('[yD]Remote Elevate answered weird message@')
        log('[yD]It might be some kind of bug...@')
        log('[yD]You can try to restart both Elevate instances@')
        exit(-1)
    
    s.send(f'NAME:{data["name"]}'.encode())
    s.recv(2).decode()
    if msg == 'NO':
        log('[r]Remote Elevate rejected us by name@')
        log('[rD]Your name seems to not be on a whitelist@')
        exit(-1)
    if msg == 'OK':
        log('[n]Remote Elevate greeted us 🤝@')
        log('[nD]Your name is on a whitelist@\n')

def sendFile(s, path):
    buff = 4096
    size = os.path.getsize(path)
    # Open and send file vin chunks
    with open(path, 'rb') as file:
        with alive_bar((size // buff) + 1, spinner='dots_waves') as bar:
            chunk = file.read(buff)
            while chunk:
                bar('Sending Project to the server')
                s.send(chunk)
                chunk = file.read(buff)

