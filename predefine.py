from simple_term_menu import TerminalMenu
from printy import printy as log
from printy import inputy as get
import argparse
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