from predefine import *

def configExec(kind, data_path):
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
    log('[y]What\'s your name? (You can make it up)@')
    newdata['name'] = input('name: ')

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
        
        yn = ['Yes', 'No']
        log('\n\n[y]Do you want to create Elevate service?@')
        log('[yD]Elevate server will then automatically restart on reboot@')
        newdata['service'] = yn[TerminalMenu(yn).show()]

        # Create a server service
        if newdata['service'] == 'Yes':
            f = ''
            try:
                f = open('/etc/systemd/system/elevate.service', 'w')
                os.system('systemctl start elevate')
                os.system('systemctl enable elevate')
            except IOError as error:
                log('[r]\nCouldn\'t create the service... reason:@')
                log(f'[rD]{error.strerror} [{error.errno}]@')
                log('[y]\nDo you want to create service file here?@')
                log('[yD]You will have to copy it to@')
                log('[yD]\t/etc/systemd/system/elevate.service@')
                log('[yD]Then enable and start it manually with@')
                log('[yD]\tsystemctl enable elevate@')
                log('[yD]\tsystemctl start elevate@')
                local = yn[TerminalMenu(yn).show()]
                if local == 'Yes':
                    f = open('elevate.service', 'w')
                else:
                    exit(-1)
            finally:
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
                    'ExecStart=/usr/bin/env python3 /opt/Elevate/elevate.py\n\n'

                    '[Install]\n'
                    'WantedBy=multi-user.target\n'
                )
                f.write(service)
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
        exit(1)
    log('[y]Let\'s quickly create a config file for this project...@')
    log('[yD]Gray values in round parentheses are default ones@\n')

    # Get IP
    data['addr'] = get('[y]Remote Address @[yD]<can be IP or domain>@: ')
    data['addr'] = forceValue('Address', data['ip'])

    # Get Port
    data['port'] = get('[y]Port @[g](3838)@: ')
    data['port'] = defaultValue('3838', data['port'])

    # Get Path
    data['path'] = get('[y]Path @[g](.)@: ')
    data['path'] = defaultValue('.', data['path'])

    # Get Secret
    data['secret'] = get('[y]Secret @[g](---)@: ')
    data['secret'] = defaultValue('', data['secret'])

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
        exit(-1)
    return data


def defaultValue(default, data):
    '''Return default value if
    no data has been provided'''
    data = data.strip()
    if len(data) == 0:
        return default
    return data

    