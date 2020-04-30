from predefine import *

def connect(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        log('[n]Found Remote Elevate@')
        log('[nD]Connected to remote Elevate server@\n')
    except socket.error as message:
        log('[r]Elevate couldn\'t connect to the remote Elevate endpoint@')
        log(f'[rD]Log: {message}@')
        sys.exit(1)
    return s


def login(s, data, config):
    s.send(f'SECR:{config["secret"]}'.encode())
    msg = s.recv(2).decode()
    if msg == 'NO':
        log('[r]Remote Elevate rejected secret@')
        log('[rD]Your secret token is invalid@')
        sys.exit(-1)
    elif msg == 'OK':
        log('[n]Remote Elevate recognized us 👋@')
        log('[nD]Your secret token is valid@\n')
    else:
        log('[y]Couldn\'t understand remote Elevate@')
        log('[yD]Remote Elevate answered weird message@')
        log('[yD]It might be some kind of bug...@')
        log('[yD]You can try to restart both Elevate instances@')
        sys.exit(-1)
    
    s.send(f'NAME:{data["name"]}'.encode())
    s.recv(2).decode()
    if msg == 'NO':
        log('[r]Remote Elevate rejected us by name@')
        log('[rD]Your name seems to not be on a whitelist@')
        sys.exit(-1)
    if msg == 'OK':
        log('[n]Remote Elevate greeted us 🤝@')
        log('[nD]Your name is on a whitelist@\n')

def sendFiles(s, path):
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
    code = 'EXIT'
    s.send(f'FILE:{code:<4096}'.encode())

def waitForServer(s):
    msg = s.recv(55).decode()
    if msg[:4] == 'ERRR':
        log('[r]Remote Elevate sent us some error:@')
        log(f'[rD]{msg.strip()}@')
        sys.exit(1)
    if msg[:4] == 'BASH':
        bash = ''
        while True:
            msg = s.recv(55).decode()
            if (msg[:9] == 'BASH:EXIT'):
                break
            bash += msg
        log(bash)
        log('\n\n[n]Done 🎉@')
        log('[nD]Successfully deployed the project@')
        


def clonePath(config, newnames):
    path = os.path.abspath(config['path'])
    isdir = os.path.isdir(path)
    if not isdir:
        log('[r]Path must be pointing to a directory 📁@')
        log(f'[rD]It seems that path ({path}) is pointing to a file@')
        sys.exit(1)
    # Copy directory to the new place
    if (os.path.exists(newnames['local-root'])):
        process.call(['rm', '-rf', newnames['local-root']])
    process.call(['cp', '-r', path, newnames['local-root']])

    # Create a client and server script
    clientp = os.path.join(newnames['local-root'], newnames['client'])
    serverp = os.path.join(newnames['local-root'], newnames['server'])
    if os.path.exists(clientp):
        log('[r]There already exists file that looks like elevate client script@')
        log('[rD]Remove file .$elevate$client.sh otherwise won\'t proceed@')
        sys.exit(-1)
    if os.path.exists(serverp):
        log('[r]There already exists file that looks like elevate server script@')
        log('[rD]Remove file .$elevate$server.sh otherwise won\'t proceed@')
        sys.exit(-1)
    with open(clientp, 'w') as file:
        file.write(config['client-script'])
    file = open(serverp, 'w')
    file.write(config['server-script'])
    file.close()
    process.call(['chmod', '777', clientp])
    process.call(['chmod', '777', serverp])
    log('[g]<-- Running Client Script -->@\n')
    process.call(['/bin/bash', clientp])
    log('\n[g]<-- Compressing Project -->@\n')
    code = os.system(f'cd {newnames["local-root"]}; zip -{config["compression"]} -r {newnames["zip"]} *')
    if code != 0:
        log('[r]Couldn\'t zip project files@')
        log('[rD]More details in Compressing Project phase@')
        exit(1)
    
    


    
