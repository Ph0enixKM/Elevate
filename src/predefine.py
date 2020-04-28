from simple_term_menu import TerminalMenu
from alive_progress import alive_bar
from printy import printy as log
from printy import inputy as get
import subprocess as process
import argparse
import socket
import json
import time
import sys
import os
import re

def exePath():
    '''Returns path to this executable'''
    relative = os.path.dirname(sys.argv[0])
    absolute = os.path.abspath(relative)
    return absolute