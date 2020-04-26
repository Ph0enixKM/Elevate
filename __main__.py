#!/usr/bin/env python3

# Project files
from predefine import * 
import configure as conf
from parser import Parser

# Global Variables
data_path = os.path.join(exePath(), 'data.json')

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

try:
    # Get the executable data
    # so that elevate can proceed
    # with given tasks
    data = getData()
    # Reconfigure Elevate
    if type(data) is int:
        if data == 0:
            conf.configExec('init', data_path)
        else:
            conf.configExec('error', data_path)
        exit(0)

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
            exit(1)
        # Try to parse the file
        with open('ele.vate', 'r') as File:
            text = File.read()
            config = Parser(text).get()
            print(config)


    # Initialize new project
    # configuration file
    elif args.operation == 'init':
        conf.configProject()
        

    elif args.operation == 'config':
        conf.configExec('none', data_path)

except KeyboardInterrupt:
    log('\n\n[g]Bye... 👋@')