from predefine import *

def configExec(kind, data_path):
    if kind == 'init':
        log('\n[n]Welcome to Elevate! 📦@')
        log('[nD]Let\'s setup your elevator 🎉@\n\n')
        time.sleep(1)
    elif kind == 'error':
        log('[r]It looks like your elevator has broken 🔻 ...@')
        log(f'[rD]Elevate can\'t parse file \'{data_path}\'@\n\n')
        time.sleep(1)
        print('Do you want to regenerate it from scratch?')
        yn = TerminalMenu(['Yes', 'No']).show()
        print('\n')
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

    log('\n\n[n]Done 🎉@')
    log('[nD]Now you can use command \'elevate\' to deploy projects!@')
    file = open(data_path, 'w')
    file.write(json.dumps(newdata, indent=4))


def configProject():
    data = {}
    content = ''
    exists = os.path.exists('ele.vate')
    if exists:
        log('[r]Couldn\'t create project config file \'ele.vate\' 🔻@')
        log('[rD]It seems that project config file already exists here@')
        exit(1)
    log('[y]Let\'s quickly create a config file for this project...@')
    log('[yD]Gray values in round parentheses are default ones@\n')
    data['ip'] = get('[y]IP @[yD]<of the remote server>@: ').strip()
    data['port'] = get('[y]Port @[g](3838)@: ').strip()
    data['path'] = get('[y]Path @[g](.)@: ').strip()
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