from pystyle import Anime, Write, Colorate, Colors, Box, Center
from time import sleep
from multiprocessing import Process, Value, freeze_support, Lock
import configparser
import requests
import json

if __name__ == '__main__':

    freeze_support()


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


    def menu():
        header()

        config = configparser.ConfigParser()
        config.read('config.ini')

        if str(config['main']['useConfig']) == "True":
            thrds = str(config['main']['threads'])
            wh = str(config['main']['webhook'])
            miner = str(config['main']['miner'])
            show = str(config['optional']['showOnlyHits'])
            Write.Print(f"\tMiner: {miner}!\n", Colors.green_to_white)
            Write.Print(f"\tThreads: {thrds}!\n", Colors.green_to_white)
            Write.Print(f"\tWebhook: CENSORED!\n", Colors.green_to_white)
            Write.Print(f"\tShow only Hits: {show}\n", Colors.green_to_white)
        else:
            print(Center.XCenter(Colorate.Vertical(Colors.blue_to_purple, Box.DoubleCube("""
                           [1] - BTC "Miner"                           
                           [2] - ETH "Miner" (Soon)
                           [3] - LTC "Miner" (Soon)
                           """))))
            
            sleep(1)
            miner = Write.Input("Miner >-->> ", Colors.green_to_blue)
            if miner != "1":
                if miner != "2":
                    if miner != "3":
                        print(Colorate.Horizontal(Colors.red_to_white, f"Only 1, 2 or 3! You selected: {miner}"))
                        quit()
            if miner == "1":
                miner = "btc"
            if miner == "2":
                miner = "eth"
            if miner == "3":
                miner = "ltc"
            thrds = Write.Input("Threads >-->> ", Colors.green_to_blue)
            
            print(Colorate.Horizontal(Colors.green_to_white, "Setup Successfull!"))
            Write.Print(f"\tMiner: {miner}!\n", Colors.green_to_white)
            Write.Print(f"\tThreads: {thrds}!\n", Colors.green_to_white)
            Write.Print(f"\tFill out config to use Webhook!\n", Colors.red_to_white)
        
        #show = Write.Input("Show only hits (y/n) >-->> ", Colors.green_to_blue)
        print(Colorate.Horizontal(Colors.green_to_white, "Starting Threads..."))


        fails = Value('i', 0)
        hits = Value('i', 0)
        lock = Lock()

        if str(config['main']['useConfig']) == "True":
            try:
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
            except:
                return None	
        try:
            response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
        except:
            return None	
        
        import btc
        import ltc
        import eth
        import title
        try:
            t = Process(target=title.titleLoop, args=(fails, lock,hits))
            if miner == "btc":
                for i in range(int(thrds)):
                    m = Process(target=btc.btcMiner, args=(fails, lock,hits))
                    m.start()
                t.start()
            elif miner == "ltc":
                for i in range(int(thrds)):
                    m = Process(target=btc.btcMiner, args=(fails, lock,hits))
                    m.start()
                t.start()
            elif miner == "eth":
                for i in range(int(thrds)):
                    m = Process(target=btc.btcMiner, args=(fails, lock,hits))
                    m.start()
                t.start()
            else:
                print(Colorate.Horizontal(Colors.red_to_white, "Your miner isnt valid!"))
                sleep(10)
                quit()
        except Exception as e:
            print(e)

    menu()
