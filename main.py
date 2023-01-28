from mnemonic import Mnemonic
import bip32utils
from bitcash import Key
import requests
import json
from discord_webhook import DiscordWebhook, DiscordEmbed
import configparser
from multiprocessing import Process, Value, freeze_support, Lock
import json

if __name__ == '__main__':

    freeze_support()
    line = 0

    config = configparser.ConfigParser()
    config.read('config.ini')

    if str(config['miner']['useConfig']) == "True":
        wh = str(config['miner']['webhook'])
        thrds = str(config['miner']['threads'])
    else:
        thrds = input("How many threads? ")
        wh = input("Discord webhook: ")
    print(f"Succesfull setup!")
    print(f"\tWebhook: {wh}")
    print(f"\tThreads: {thrds}")


    webhook_url = wh

    data = {
    "content": None,
    "embeds": [
        {
        "title": f"Threads: {thrds}",
        "description": "Good Luck!",
        "color": 6749952,
        "author": {
            "name": "Miner Started!"
        }
        }
    ],
    "username": "2xWallet",
    "avatar_url": "https://cdn.discordapp.com/attachments/1062796452885188670/1068636566605537330/image.png",
    "attachments": []
    }

    headers = {'Content-type': 'application/json'}

    response = requests.post(webhook_url, data=json.dumps(data), headers=headers)


    print("Starting threads...")
    import checker
    import title
    lock = Lock()
    fails = Value('i', 0)  
    for i in range(int(thrds)):
        p = Process(target=checker.check, args=(fails, lock))
        p.start()
    t = Process(target=title.titleLoop, args=(fails, lock))
    t.start()
    
