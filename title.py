from mnemonic import Mnemonic
import bip32utils
from bitcash import Key
import requests
import json
from discord_webhook import DiscordWebhook, DiscordEmbed
from multiprocessing import Process, Value, freeze_support, Lock
import os
from datetime import datetime, date
import configparser
from time import sleep
from pystyle import Anime, Write, Colorate, Colors, Box, Center
from sys import platform


def header():
    print(Center.XCenter(Colorate.Vertical(Colors.purple_to_red, """
    $$$$$$\            $$\      $$\           $$\ $$\            $$\     
    $$  __$$\           $$ | $\  $$ |          $$ |$$ |           $$ |    
    \__/  $$ |$$\   $$\ $$ |$$$\ $$ | $$$$$$\  $$ |$$ | $$$$$$\ $$$$$$\   
    $$$$$$  |\$$\ $$  |$$ $$ $$\$$ | \____$$\ $$ |$$ |$$  __$$\\_$$  _|  
    $$  ____/  \$$$$  / $$$$  _$$$$ | $$$$$$$ |$$ |$$ |$$$$$$$$ | $$ |    
    $$ |       $$  $$<  $$$  / \$$$ |$$  __$$ |$$ |$$ |$$   ____| $$ |$$\ 
    $$$$$$$$\ $$  /\$$\ $$  /   \$$ |\$$$$$$$ |$$ |$$ |\$$$$$$$\  \$$$$  |
    \________|\__/  \__|\__/     \__| \_______|\__|\__| \_______|  \____/ 
                                                                        
    """)))

def titleLoop(fails, lock, hits):
    config = configparser.ConfigParser()
    config.read('config.ini')
    show = 0
    if str(config['main']['useConfig']) == "True":
        show = str(config['optional']['showOnlyHits'])
    now = datetime.now()
    timeB = now.strftime("%H:%M:%S") 
    today = date.today()
    c = 0
    z = 0
    cps = 0
    while True:
        if z == 1:
            cps = fails.value - c
        terminal_title = f'2xWallet >->> NoBal: {fails.value}  /  Started: {today}  CPS: {cps}'
        print(f'\33]0;{terminal_title}\a', end='', flush=True)  
        
        if show == "True":
            if platform == "linux" or platform == "linux2":
                os.system('clear')
            else:
                os.system('cls')
                
            header()
            print(Center.XCenter(Colorate.Vertical(Colors.blue_to_purple, Box.DoubleCube(f"""
                           [Hits] - {hits.value}                           
                           [NoBal] - {fails.value}
                           [CPS] - {cps}
            Use webhook to get notifyed on a hit :3
                           """))))
        c = fails.value
        z = 1
        sleep(1)
        
