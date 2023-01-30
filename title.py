from mnemonic import Mnemonic
import bip32utils
from bitcash import Key
import requests
import json
from discord_webhook import DiscordWebhook, DiscordEmbed
from multiprocessing import Process, Value, freeze_support, Lock
import os
from datetime import datetime, date
from time import sleep

def titleLoop(fails, lock):
    now = datetime.now()
    timeB = now.strftime("%H:%M:%S") 
    today = date.today()
    c = 0
    z = 0
    cps = 0
    while True:
        if z == 1:
            cps = fails.value - c
        os.system(f'title 2xWallet >->> NoBal: {fails.value}  /  Started: {today}  CPS: {cps}')
        c = fails.value
        z = 1
        sleep(1)
        