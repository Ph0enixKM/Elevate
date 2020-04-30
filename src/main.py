#!/usr/bin/env python3

# Project files
from parser import Parser
import configure as conf
from predefine import * 
import client
import server

# Global Variables
data_path = os.path.join(exePath(), 'data.json')
exec_path = os.path.join(exePath(), os.path.basename(sys.argv[0]))
newnames = {
    'local-root': '/tmp/elevate-project', 
    'client': 'elevate-client.sh',
    'server': 'elevate-server.sh',
    'zip': 'dist.zip',
    'dir' : 'dist'
}

def getData():
    '''Returns data JSON file if it's corrupted 
    returns 1 if the data file doesn't exist returns 0'''
    # Get path to the data file
    global data_path
    exists = os.path.exists(data_path)
    # If the data file doesn't exist
    if not exists:
        return 0
    # Try to open data file
    with open(data_path, 'r', encoding = 'utf-8') as File:
        content = File.read()
        data = {}
        try:
            data = json.loads(content)
        except ValueError:
            return 1
        return data

# Message for other non-Linux kernel based systems
if not (platform.system() == 'Linux'):
    log('[y]Warning! Elevate detected this script is running on other kernel than Linux.')
    log('[yD]It\'s highly recommended to change your OS to Linux based before proceeding.')
    input('')

try:
    # Get the executable data
    # so that elevate can proceed
    # with given tasks
    data = getData()
    # Socket instance
    s = None
    # Reconfigure Elevate
    if type(data) is int:
        if data == 0:
            conf.configExec('init', data_path, exec_path)
        else:
            conf.configExec('error', data_path, exec_path)
        sys.exit(0)

    # Available ops
    ops = []
    if data['kind'] == 'Client':
        ops = ['deploy', 'config', 'init']
    elif data['kind'] == 'Server':
        ops = ['serve', 'config']

    # Get the arguments
    parser = argparse.ArgumentParser(
        'elevate',
        epilog='<-- If nothing is passed, then \'deploy\' command kicks in. -->'
    )
    parser.add_argument(
        'operation', 
        help=f'Kind of an operation {ops}', 
        nargs='?', 
        default=ops[0]
    )
    args = parser.parse_args()


    # Deploy project based on the
    # configuration file
    if args.operation == 'deploy':

        # Check if project config file exists
        exists = os.path.exists('ele.vate')
        if not exists:
            log('[r]Couldn\'t find project config file \'ele.vate\' 🔍@')
            log('[rD]Make sure you are in the root directory of your project@')
            log('[rD]\nYou can create a new config with command:@')
            log('[rD]    elevate init@')
            sys.exit(1)
        # Try to parse the file
        with open('ele.vate', 'r') as file:
            text = file.read()
            config = Parser(text).get()
            client.clonePath(config, newnames)
            log('[g]\n<-- Connecting with remote Elevate -->@\n')
            s = client.connect(config['addr'], config['port'])
            client.login(s, data, config)
            log('[g]\n<-- Sending Project Files -->@\n')
            zipFile = os.path.join(newnames['local-root'], newnames['zip'])
            client.sendFiles(s, zipFile)
            log('[g]\n<-- Running Server Script -->@\n')
            client.waitForServer(s)
    
    if args.operation == 'serve':
        s = server.listen(data)
        while True:
            client, addr = s.accept()
            isAuth = server.auth(client, data)
            if not isAuth:
                continue
            server.recvFiles(client, data, newnames)
            server.unboxProject(client, data, newnames)


    # Initialize new project
    # configuration file
    elif args.operation == 'init':
        conf.configProject()
        
    # Configure Illiade
    # From scratch
    elif args.operation == 'config':
        conf.configExec('none', data_path, exec_path)

    

except KeyboardInterrupt:
    log('\n\n[g]Bye... 👋@')