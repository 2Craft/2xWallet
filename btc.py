from pystyle import Anime, Write, Colorate, Colors, Box, Center
from time import sleep
from multiprocessing import Process, Value, freeze_support, Lock
import configparser
from datetime import datetime, date
from mnemonic import Mnemonic
import bip32utils
import random
import requests
import json
import urllib3


def HitWebhook(bal, wallet, WIF, words):
    if str(config['main']['useConfig']) == "True":
        try:
            config = configparser.ConfigParser()
            config.read('config.ini')
            webhook_url = str(config["main"]["webhook"])

            data = {
            "content": None,
            "embeds": [
                {
                "title": f"2xWallet",
                "description": f"HIT! | WIF: {str(WIF)} | Bal: {bal} | Address: {str(wallet)} | Seed: {str(words)}",
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
        except:
            return None
    else:
        return None

def btcMiner(fails, lock, hits):
    config = configparser.ConfigParser()
    config.read('config.ini')
    if str(config['main']['useConfig']) == "True":
        show = str(config['optional']['showOnlyHits'])
        if show == "True":
            show = 1
        else:
            show = 0
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    l = "balance"
    now = datetime.now()
    timeB = now.strftime("%H:%M:%S") 
    startedDate = date.today()
    if str(config["optional"]["useProxy"]) == "True":
        changeProxRatio = int(config["optional"]["changeProxyRatio"])
        with open("proxys.txt") as f:
            proxies = [line.strip() for line in f]
    #print("Starting thread..")
    while True:
        if str(config["optional"]["useProxy"]) == "True":
            if changeProxRatio == int(config["optional"]["changeProxyRatio"]):
                proxy = random.choice(proxies)
                http = f'http://{proxy}'
                https = f'https://{proxy}'
                prox = {
                        'http': f'{http}'
                    }
                changeProxRatio = 0
        mnemonic = Mnemonic("english")
        words = mnemonic.generate(strength=256)
        seed = mnemonic.to_seed(words)

        key = bip32utils.BIP32Key.fromEntropy(seed)
        address = key.Address()
        WIF = key.WalletImportFormat()

        #Check Bal
        if str(config["optional"]["useProxy"]) == "True":
            response = requests.get(f"https://blockchain.info/balance?active={address}", proxies=prox, verify=False)
        else:
            response = requests.get(f"https://api-r.bitcoinchain.com/v1/address/{address}")

        
        lol = response.text
        if l in lol:
            try:
                ls = json.loads(lol)
                for balance in ls:
                    bal = balance["balance"]
                    if bal > 0:
                        try:
                            hits.value += 1
                        except:
                            continue
                        f = open("hits.txt", "a")
                        data = (f'New Hit! | balance: {bal} | Wallet: {address} | WIF: {WIF} | Phrase: {words}')
                        f.write(str(data) + "\n")
                        f.close()
                        print(Colorate.Color(Colors.green, f"[ / ] - HIT: {address} | Balance: {bal} | WIF: {WIF} | Phrase: {words}"))  
                        try:
                            HitWebhook(bal, address, WIF, words)
                        except:
                            print("Webhook Error!")
                            continue
                        input("")
                    else:
                        if show != 1:
                            print(Colorate.Color(Colors.red, f"[{fails.value}] - Invalid: {address} | WIF: {WIF} | Phrase: {words}"))  
                        fails.value += 1
                else:
                    if show != 1:
                        print(Colorate.Color(Colors.red, f"[{fails.value}] - Invalid: {address} | WIF: {WIF} | Phrase: {words}"))  
                    fails.value += 1
            except:
                print("Blocked...")
        else:
            if show != 1:
                print(Colorate.Color(Colors.red, f"[{fails.value}] - Invalid: {address} | WIF: {WIF} | Phrase: {words}"))  
            fails.value += 1


        #print(f"Add: {address} | WIF: {WIF} | Phrase: {words}")

    