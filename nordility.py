'''
    Author: Cason Konzer
    Module: nordility
    -- Part of: citegres
    Developed for: Advance Database Concepts & Applications

    Function: Provides an interface for VPN switching
    Version: 3.0
    Dated: December 2, 2023
'''

# IMPORTS
import time
import subprocess
import numpy as np
import logging
import sys

# STATIC SET
logging.basicConfig(stream=sys.stdout, encoding='utf-8', level=logging.INFO)
pyLogger = logging.getLogger(name='nordility_debug')

# STATIC VARS
NORDVPN_EXE_PATH = 'C:/Program Files/NordVPN/NordVPN.exe'

NORDVPN_GROUP_LIST_FULL = [
    'Albania', 'Germany', 'Poland',
    'Argentina', 'Greece', 'Portugal',
    'Australia', 'Hong_Kong', 'Romania',
    'Austria', 'Hungary', 'Serbia',
    'Belgium', 'Iceland', 'Singapore',
    'Bosnia_And_Herzegovina', 'Indonesia', 'Slovakia',
    'Brazil', 'Ireland', 'Slovenia',
    'Bulgaria', 'Israel', 'South_Africa',
    'Canada', 'Italy',
    'Chile', 'Japan', 'Spain',
    'Colombia', 'Latvia', 'Sweden',
    'Costa_Rica' 'Lithuania', 'Switzerland',
    'Croatia', 'Luxembourg', 'Taiwan',
    'Cyprus', 'Malaysia', 'Thailand',
    'Czech_Republic', 'Mexico', 'Turkey',
    'Denmark', 'Moldova', 'Ukraine',
    'Estonia', 'Netherlands', 'United_Kingdom',
    'Finland', 'New_Zealand', 'United_States',
    'France', 'North_Macedonia', 'Vietnam',
    'Georgia', 'Norway'
]

NORDVPN_GROUP_LIST_FAST = [
    'Germany', 'Poland',
    'Greece', 'Austria', 'Hungary',
    'Belgium', 'Brazil', 'Ireland',
    'Canada', 'Italy',
    'Japan', 'Spain',
    'Colombia', 'Sweden', 'Switzerland',
    'Luxembourg', 'Mexico', 'Denmark',
    'Netherlands', 'United_Kingdom',
    'Finland', 'United_States',
    'France', 'Norway'
]

# BASIC DEFS
def connect_vpn_server(status=True):
    '''
    Connects to a random Nord VPN server, usually defaults to best possible
    '''
    try:
        subprocess.Popen(f'{NORDVPN_EXE_PATH} -c')
        pyLogger.info('VPN Connected')
        if status:
            return 'VPN Connected'
    except Exception as E:
        pyLogger.error('%s \nexception in connect_vpn_server' % str(E))
        if status:
            return 'VPN Failed to Connect'

def disconnect_vpn_server(status=True):
    '''
    Disconnect Nord VPN
    '''
    try:
        subprocess.Popen(f'{NORDVPN_EXE_PATH} -d')
        pyLogger.info('VPN Disconnected')
        if status:
            return 'VPN Disconnected'
    except Exception as E:
        pyLogger.error('%s \nexception in disconnect_vpn_server' % str(E))
        if status:
            return 'VPN Failed to Disconnect'

def change_vpn_server(speed='fast', fast_reset=10, default_reset=30, status=True):
    '''
    Select a new Nord VPN server form a full or fast list, timeouts are set respectively
    '''
    try:
        if speed == 'fast':
            GROUP = NORDVPN_GROUP_LIST_FAST[np.random.randint(0,len(NORDVPN_GROUP_LIST_FAST)-1)]
            subprocess.Popen(f'{NORDVPN_EXE_PATH} -c -g "{GROUP}"')
            time.sleep(fast_reset)
        else:
            GROUP = NORDVPN_GROUP_LIST_FULL[np.random.randint(0,len(NORDVPN_GROUP_LIST_FULL)-1)]
            subprocess.Popen(f'{NORDVPN_EXE_PATH} -c -g "{GROUP}"')
            time.sleep(default_reset)
        pyLogger.info('VPN Redirected to %s' % GROUP)
        if status:
            return f'VPN Connection Successfully Redirected to {GROUP}'
    except Exception as E:
        pyLogger.error('%s \nexception in change_vpn_server' % str(E))
        if status:
            return f'VPN Connection Failed to Redirect to {GROUP}'
