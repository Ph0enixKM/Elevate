from predefine import *
from words.rand_words import words_rand

def configExec(kind, data_path, exec_path):
    '''Configurate elevate executable'''
    if kind == 'init':
        log('\n[n]Welcome to Elevate! 📦@')
        log('[nD]Let\'s setup your elevator 🎉@\n\n')
    elif kind == 'error':
        log('[r]It looks like your elevator has broken 🔻 ...@')
        log(f'[rD]Elevate can\'t parse file \'{data_path}\'@\n\n')
        print('Do you want to regenerate it from scratch?')
        yn = TerminalMenu(['Yes', 'No']).show()
        print('\n')
    elif kind == 'none':
        log('\n[n]Let\'s reconfigure Elevate! 📦@')
        log('[nD]Elevate will be reconfigured from scratch@\n\n')
    else:
        raise ValueError('Bad kind type: ' + kind)

    newdata = {}
    log('[yD]Let me ask you couple of questions...@')
    log('[y]What\'s your name? (You can make it up)@[yD](max 35 characters)@')
    newdata['name'] = input('name: ')
    if (len(newdata['name']) > 35):
        log('[r]Name must be at maximum 35 characters long@')
        log(f'[rD]Name \'{newdata["name"]}\' is way too long@')
        sys.exit(1)

    options = ['Client', 'Server']
    log('\n\n[y]How do you want to use this program?@')
    log('[yD]Are you on a local machine or server right now?...@')

    newdata['kind'] = options[TerminalMenu(options).show()]
    print('kind:', newdata['kind'])

    # Configure for server
    if newdata["kind"] == 'Server':
        log('\n\n[y]What port are you going to be using?@')
        log('[yD]Default port is 3838...@')
        newdata['port'] = get('port: ', type='int')
        
        log('\n\n[y]Where do you wish to unpack new projects?@')
        log('[yD]This directory will contain your project and old version files@')
        newdata['path'] = get('path: ')
        newdata['path'] = forceValue('Path', newdata['path'])
        if not os.path.exists(newdata['path']):
            log('[r]It seems that provided path does not exist@')
            log('[rD]Please provide path that already exists@')
            sys.exit(1)
        newdata['path'] = os.path.abspath(newdata['path'])

        log('\n\n[y]Create a secret key (It\'s like a password)@')
        log('[yD]This password will be used by users to connect with the server @[yD](max 35 characters)@')
        log('[yD]Leaving this field empty will not specify secret but anyone will be able to connect with the server, which leaves a security hole...@')
        log(f'\n[yD]What about: {"-".join(words_rand())}?@')
        newdata['secret'] = get('secret: ')
        if (len(newdata['secret']) > 35):
            log('[r]Secret must be at maximum 35 characters long@')
            log(f'[rD]Secret \'{newdata["secret"]}\' is way too long@')
            sys.exit(1)

        yn = ['Yes', 'No']
        log('\n\n[y]Do you want to create Elevate service?@')
        log('[yD]Elevate server will then automatically restart on reboot and run in background@')
        newdata['service'] = yn[TerminalMenu(yn).show()]
        print('service:', newdata['service'])

        # Create a server service
        if newdata['service'] == 'Yes':
            isServ = False
            f = ''
            if os.path.exists('/etc/systemd/system/elevate.service'):
                log('[r]Elevate service already exists!@')
                log('[rD]It seems that there is another elevate working already...@')
                log('[rD]Or old elevate instance left an old service file@')
                log('[rD]\nPlease clean it up using these commands as a root@')
                log('[rD]\tsudo systemctl disable elevate@')
                log('[rD]\tsudo rm /etc/systemd/system/elevate.service@')
                sys.exit(1)
            try:
                f = open('/etc/systemd/system/elevate.service', 'w')
                isServ = True
            except IOError as error:
                log('[r]\nCouldn\'t create the service... reason:@')
                log(f'[rD]{error.strerror} [{error.errno}]@')
                log('[y]\nDo you want to create service file here?@')
                log('[yD]You will have to copy it to@')
                log('[yD]\t/etc/systemd/system/elevate.service@')
                log('[yD]Then enable and start it manually with (as root)@')
                log('[yD]\tsystemctl enable elevate@')
                log('[yD]\tsystemctl start elevate@')
                log('[yD]\nOtherwise elevate will exit so you can run it@')
                log('[yD]with root privileges (sudo elevate)@')
                local = yn[TerminalMenu(yn).show()]
                print('local:', local)
                if local == 'Yes':
                    f = open('elevate.service', 'w')
                else:
                    log('[nD]\nSee you in a while 👋@')
                    sys.exit(1)
            service = (
                '[Unit]\n'
                'Description=Elevate service\n'
                'After=network.target\n'
                'StartLimitIntervalSec=0\n\n'

                '[Service]\n'
                'Type=simple\n'
                'Restart=always\n'
                'RestartSec=1\n'
                'User=root\n'
                'ExecStart='+ exec_path +'\n\n'

                '[Install]\n'
                'WantedBy=multi-user.target\n'
            )
            f.write(service)
            if isServ:
                log('\n\n[n]Service Created@')
                log('[nD]In order to enable it run the following comamnds:@')
                log('[nD]\tsudo systemctl enable elevate@')
                log('[nD]\tsudo systemctl start elevate@')
            f.close()

    log('\n\n[n]Done 🎉@')
    log('[nD]Now you can use command \'elevate\' to deploy projects!@')
    file = open(data_path, 'w')
    file.write(json.dumps(newdata, indent=4))


def configProject():
    '''Configurate project'''
    data = {}
    content = ''
    exists = os.path.exists('ele.vate')
    if exists:
        log('[r]Couldn\'t create project config file \'ele.vate\' 🔻@')
        log('[rD]It seems that project config file already exists here@')
        sys.exit(1)
    log('[y]Let\'s quickly create a config file for this project...@')
    log('[yD]Gray values in round parentheses are default ones@\n')

    # Get IP
    data['addr'] = get('[y]Remote Address @[yD]<can be IP or domain>@: ')
    data['addr'] = forceValue('Address', data['addr'])

    # Get Port
    data['port'] = get('[y]Port @[g](3838)@: ')
    data['port'] = defaultValue('3838', data['port'])
    if not data['port'].isnumeric():
        log('[r]Given port is invalid@')
        log('[rD]Ports are usually of numeric type@')
        sys.exit(1)

    # Get Path
    data['path'] = get('[y]Path @[g](.)@: ')
    data['path'] = defaultValue('.', data['path'])

    # Get Secret
    data['secret'] = get('[y]Secret @[g]()@: ')
    data['secret'] = defaultValue('', data['secret'])

    # File Compresson Level
    data['compression'] = get('[y]Project Compression Level @[yD]<0-9>@[g](5)@: ')
    data['compression'] = defaultValue(5, data['compression'])
    if not str(data['compression']).isdigit():
        log('[r]Level between 0 and 5 is required@')
        sys.exit(1)

    log('\n\n[n]Done 🎉@')
    log(re.sub(r'\s+', ' ', """
        [nD]Now you can see the \'ele.vate\' file and define scripts 
        to execute here before deployment and once files are unpacked on the server@
        """)[1:-1])
    content += '<-- CLIENT -->\n\n'
    content += 'echo "I\'m about to send the files..."\n\n'
    content += '<-- CONFIG -->\n'
    content += json.dumps(data, indent=4) + '\n'
    content += '<-- SERVER -->\n\n'
    content += 'echo "Installing packages here..."\n'
    content += 'echo "Restarting service that runs the server..."\n\n'
    file = open('ele.vate', 'w')
    file.write(content)


def forceValue(name, data):
    '''Throw error and terminate
    If no data has been provided'''
    data = data.strip()
    if len(data) == 0:
        log(f'[r]You didn\'t provide required field {name}@')
        log(f'[rD]{name} field has no default value candidate@')
        sys.exit(1)
    return data


def defaultValue(default, data):
    '''Return default value if
    no data has been provided'''
    data = data.strip()
    if len(data) == 0:
        return default
    return data

    