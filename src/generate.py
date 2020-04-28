from simple_term_menu import TerminalMenu
    
def start():
    print('Welcome to Elevate! 📦')
    print('Let\'s setup your elevator 🎉\n\n')
    print('How are you going to use this Elevate app?')
    terminal_menu = TerminalMenu(["client", "server"])
    result = terminal_menu.show()

class Config:
    def __init__(self):
        pass
    
    def run(self):
        print('Let\'s setup your elevator 🎉\n\n')
        print('# What is your name? (You can make it up)')
        name = input('Name: ')
        print('# How are you going to use this Elevate app?')
        usage = TerminalMenu(["client", "server"]).show()

Config().run()
