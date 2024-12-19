import re
import os
import pycurl
import certifi
import json
import glob
import urllib.parse
import sub.common as common
from io import BytesIO
from termcolor import colored
from sub.printer import print_user_info_message

COOKIE_DIR = './cookies/'

async def sign_main(email, password):
    logged = False
    user_info = await get_user_info()
    if '{"data":{"' in user_info:
        user_info = json.loads(user_info)
        print('Previous session detected!')
        # print('User: ' + colored(user_info['data']['email'], 'blue'))

        while True:
            print('\n1 - Resume and skip login')
            print('2 - Drop and connect a new account')
            # Prompt for resume
            resume = input('Enter your choice: ')
            if resume == '1':
                # print_user_info_message(user_info)
                logged = True
                break # Exit the loop on valid selection
            elif resume == '2':
                print(colored('Dropping previous session...', 'yellow'))
                [os.remove(f) for f in glob.glob(f'{COOKIE_DIR}*qxbroker.com.txt')]
                user_info = '{"message":"Unauthenticated."}'
                break # Exit the loop on valid selection
            else:
                print(colored('Invalid choice. Please select 1 or 2.', 'yellow'))
    if not logged and '{"message":"Unauthenticated."}' in user_info:
        while True:
            # Prompt for email
            email = input('Enter your email: ')
            if validate_email(email):
                break # Exit the loop on valid selection
            else:
                print(colored('Invalid email format.', 'yellow'))
        # Prompt for password
        password = input('Enter your password: ')

        # Attempt login
        sign_in_page = await login()

        if '<input type="hidden" name="_token" value="' in sign_in_page:
            token = common.gstrb ('<input type="hidden" name="_token" value="', '"', sign_in_page)
            sign_in_page = await login(email, password, token)

            if "Please enter the PIN-code we've just sent to your email" in sign_in_page:
                token = common.gstrb ('<input type="hidden" name="_token" value="', '"', sign_in_page)
                while True:
                    # Prompt for PIN-code
                    code = input("Please enter the PIN-code we've just sent to your email: ")
                    if validate_pin_code(code):
                        break # Exit the loop on valid selection
                    else:
                        print(colored('Invalid 6-digit code.\nPlease enter a valid 6-digit code.', 'yellow'))
                sign_in_page = await login(email, password, token, code)

        # Get user info
        user_info = await get_user_info()
        if '{"data":{"' in user_info:
            user_info = json.loads(user_info)
            print_user_info_message(user_info)
            logged = True
    return logged

async def login(email='', password='', token='', code='', proxy=''):
    buffer = BytesIO()

    body = {
        '_token': token,
        'email': email,
        'password': password,
        'remember': '1'
    }
    if code:
        body['keep_code'] = '1'
        body['code'] = code

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    }
    if token:
        headers['Content-Type'] = 'application/x-www-form-urlencoded'

    params = {
        'url': 'https://qxbroker.com/en/sign-in/',
        'proxy': proxy,
        'buffer': buffer,
        'headers': common.curl_headers(headers),
    }
    if token:
        params['postfields'] = urllib.parse.urlencode(body)

    c = common.curl_setup(params)

    try:
        c.perform()
    except pycurl.error as e:
        return f'Error: {e}'
    finally:
        c.close()

    return buffer.getvalue().decode('utf-8')

async def get_user_info(proxy=''):
    return await common.get_data ('https://qxbroker.com/api/v1/cabinets/digest', proxy)

def validate_email(email):
    if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        return True
    return False
# Function to validate 6-digit PIN-code
def validate_pin_code(pincode):
    if re.match(r'^\d{6}$', pincode):
        return True
    return False