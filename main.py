# Project files
from predefine import * 
import configure as conf
import parser

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


# Available ops
ops = ['deploy', 'config', 'init']
# Get the arguments
parser = argparse.ArgumentParser(
    'elevate',
    epilog='<-- If nothing is passed, then \'deploy\' command kicks in. -->'
)
parser.add_argument(
    'operation', 
    help=f'Kind of an operation {ops}', 
    nargs='?', 
    default='deploy'
)
args = parser.parse_args()

# Run deploy
if args.operation == 'deploy':
    data = getData()
    # Reconfigure Elevate
    if type(data) is int:
        if data == 0:
            conf.configExec('init', data_path)
        else:
            conf.configExec('error', data_path)
        exit(0)

    # Check if project config file exists
    exists = os.path.exists('ele.vate')
    if not exists:
        log('[r]Couldn\'t find project config file \'ele.vate\' 🔍@')
        log('[rD]Make sure you are in the root directory of your project@')


elif args.operation == 'init':
    conf.configProject()
    

