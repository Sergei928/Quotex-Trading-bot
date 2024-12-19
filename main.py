import os
import sys
import glob
import json
import asyncio
import colorama
from termcolor import colored
import sub.common as common
from datetime import datetime, timedelta
from sub.init_window import init
from sub.signin import sign_main
from sub.run_browser import run_browser_script
from sub.print_welcome_message import print_welcome_message
from playwright._impl._errors import TargetClosedError

colorama.init()

ARGS = sys.argv[1:]
CACHE_DIR = './cache/'
CONFIG_DIR = './config/'
COOKIE_DIR = './cookies/'
RESULT_DIR = './results/'

init()

async def main():
    [os.remove(f) for f in glob.glob(f'{CACHE_DIR}*.json')]
    [os.remove(f) for f in glob.glob(f'{CONFIG_DIR}*.json')]
    print_welcome_message()
    email = "nayrananda1998@gmail.com"
    password = "Ayush@9028"
    while True:
        logged = await sign_main(email, password)
        
        if logged:
            user_input = {
                "account_type": "demo",
                "trading_type": "compounding",
                "bet_level": 3,
                "bet_amounts": [
                    100,
                    300,
                    550
                ],
                "financial_instruments": "cryptocurrency",
                "market_type": "otc",
                "time_option": 1,
                "trade_time": 60,
                "minimum_return": 90,
                "trade_option": "random",
                "profit_target": 1000,
                "loss_target": 300
            }
            common.file_put_contents (f'{CONFIG_DIR}user_input.json', json.dumps(user_input))
            try:
                await run_browser_script(user_input)
            except TargetClosedError:
                print("Context or page is closed")
            except Exception as e:
                print(f"An error occurred while running the browser script: {e}")
            break # Exit Main loop
        else:
            print(colored('Error connecting to qxbroker.com server.', 'red'))

if __name__ == '__main__':
    try:
        asyncio.run(main())
    finally:
        input('Done !')
        os._exit(0)