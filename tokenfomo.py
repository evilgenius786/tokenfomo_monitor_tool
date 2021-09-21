import datetime
import json
import os
import threading
import time
import traceback

import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater

t = 10
tokenfomo = 'https://tokenfomo.io/?f='
proxy={}
testing = False


def monitor_eth():
    tkn = 'Token1'
    chat_id = -1001571309828
    updater = Updater(tkn, use_context=True)
    chart = 'https://www.dextools.io/app/uniswap/pair-explorer/'
    old = []
    filled = False
    while True:
        try:
            print(datetime.datetime.now(), "eth", 'Checking...')
            # with open('tokenfomo.txt', encoding='utf8') as tkn:
            #     content = tkn.read()
            content = requests.get(tokenfomo + "ethereum", proxies=proxy).content
            soup = BeautifulSoup(content, 'lxml')
            for tr in soup.find_all('tr')[:-1]:
                td = tr.find_all('td')
                name = td[0].text
                if not filled:
                    old.append(name)
                elif name not in old:
                    data = {"name": name, "chart": chart + td[4].find('a')['href'].split("=")[1],
                            "etherscan": td[3].find('a')['href'], "uniswap": td[4].find('a')['href']}
                    print(datetime.datetime.now(), "eth", json.dumps(data, indent=4))
                    old.append(name)

                    updater.bot.sendMessage(chat_id=chat_id, text=f"""<b>{data['name']}</b>
<a href="{data['etherscan']}">Etherscan</a>
<a href="{data['uniswap']}">Uniswap</a>
<a href="{data['chart']}">Chart</a>""", parse_mode="html", disable_web_page_preview=True)
                    if testing:
                        input('Press any key...')
            if not filled:
                filled = True
                print("Old coins", old)
            if testing:
                old.pop(0)
        except:
            traceback.print_exc()
        time.sleep(t)


def monitor_bsc():
    tkn = 'Token2'
    chat_id = -1001589924110
    updater = Updater(tkn, use_context=True)
    chart = 'https://poocoin.app/tokens/'
    old = []
    filled = False
    while True:
        try:
            print(datetime.datetime.now(), "bsc", 'Checking...')
            # with open('tokenfomo.txt', encoding='utf8') as tkn:
            #     content = tkn.read()
            content = requests.get(tokenfomo + "bsc", proxies=proxy).content
            soup = BeautifulSoup(content, 'lxml')
            for tr in soup.find_all('tr')[:-1]:
                td = tr.find_all('td')
                name = td[0].text
                if not filled:
                    old.append(name)
                elif name not in old:
                    data = {"name": name, "chart": chart + td[4].find('a')['href'].split("=")[1],
                            "BscScan": td[3].find('a')['href'], "PancakeSwap": td[4].find('a')['href']}
                    print(datetime.datetime.now(), "bsc", json.dumps(data, indent=4))
                    updater.bot.sendMessage(chat_id=chat_id, text=f"""<b>{data['name']}</b>
<a href="{data['BscScan']}">BscScan</a>
<a href="{data['PancakeSwap']}">PancakeSwap</a>
<a href="{data['chart']}">Chart</a>""", parse_mode="html", disable_web_page_preview=True)
                    old.append(name)
                    if testing:
                        input('Press any key...')
            if not filled:
                filled = True
                print("Old coins", old)
            if testing:
                old.pop(0)
        except:
            traceback.print_exc()
        time.sleep(t)


def main():
    os.system('color 0a')
    logo()
    t1 = threading.Thread(target=monitor_eth)
    t1.start()
    time.sleep(t / 2)
    t2 = threading.Thread(target=monitor_bsc())
    t2.start()
    t1.join()
    t2.join()


def logo():
    print("""
    ___________     __                 ___________                    
    \__    ___/___ |  | __ ____   ____ \_   _____/___   _____   ____  
      |    | /  _ \|  |/ // __ \ /    \ |    __)/  _ \ /     \ /  _ \r
      |    |(  <_> )    <\  ___/|   |  \|     \(  <_> )  Y Y  (  <_> )
      |____| \____/|__|_ \\\\___  >___|  /\___  / \____/|__|_|  /\____/ 
                        \/    \/     \/     \/              \/        
=============================================================================
                        TokenFomo monitor tool.
                Developed by: fiverr.com/muhammadhassan7
=============================================================================
""")


if __name__ == '__main__':
    main()
