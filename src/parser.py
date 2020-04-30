from predefine import *

class Parser:
    '''Class that compiles config 
    file into a readable dict'''

    def __init__(self, content):
        lex = self.lexer(content)
        self.conf = self.parser(lex)


    def lexer(self, content):
        '''Separate lines and 
        put them into a list'''
        self.lines = []
        self.line = ''
        for item in content:
            if item == '\n':
                self.lines.append(self.line)
                self.line = ''
            else:
                self.line += item
        return self.lines


    def parser(self, lex):
        '''Parse lines and extract 
        data out of them'''
        client = ''
        config = ''
        server = ''
        # Phase variables
        phase = 0
        phases = [
            r'\s*<--\s*CLIENT\s*-->\s*',
            r'\s*<--\s*CONFIG\s*-->\s*',
            r'\s*<--\s*SERVER\s*-->\s*',
            r'$.'
        ]
        # If file is just too short
        if (len(lex) < 4):
            log('[r]Bad config file contents@')
            log('[rD]Config file is too short@')
            sys.exit(1)
        # Iterate the lex
        for item in lex:
            # Next Phase
            if re.match(phases[phase], item):
                phase += 1
                continue
            # If it's a client
            # shellscript context
            if phase == 1:
                client += item + '\n'
            # If it's a config
            # shellscript context
            if phase == 2:
                config += item
            # If it's a server
            # shellscript context
            if phase == 3:
                server += item + '\n'
        # If no config loaded than it means
        # that the file is broken
        if (len(config) < 2):
            log('[r]Bad config file contents@')
            log('[rD]Couldn\'t find config section@')
            sys.exit(1)
        # Load config to json
        conf = {}
        try:
            conf = json.loads(config)
        except ValueError:
            log('[r]Elevate failed to decode json in config file@')
            log('[rD]CONFIG\'s json data is written incorrectly@')
            sys.exit(1)
        conf['client-script'] = client
        conf['server-script'] = server
        return conf

    # Returns parsed
    # config file
    def get(self):
        return self.conf
        
# with open('ele.vate', 'r', encoding = 'utf-8') as File:
#     content = File.read()
#     print(Parser(content).get())