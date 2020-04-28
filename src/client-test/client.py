from alive_progress import alive_bar
import os
import socket
import time

def connect(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((socket.gethostname(), 3838))
    except socket.error as message:
        log('[r]Elevate couldn\'t connect to the remove Elevate endpoint@')
        log('[r]Log:@')
        log(f'[rD]Log:{message}@')
    return s



# buff = 1024
# size = os.path.getsize('illi.zip')

# with open('illi.zip', 'rb') as file:
#     with alive_bar((size // buff) + 1, spinner='dots_waves') as bar:
#         chunk = file.read(buff)
#         while chunk:
#             bar('Sending Project to the server')
#             # time.sleep(0.0001)
#             s.send(chunk)
#             chunk = file.read(buff)
#         s.close()