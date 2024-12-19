import re
import pycurl
import certifi
from io import BytesIO

COOKIE_DIR = './cookies/'

def gstrb(from_str, to_str, strs, offset=0):
    offset_start = (strs.find(from_str, offset) + len(from_str)) if (offset_start := strs.find(from_str, offset)) != -1 else offset
    offset_end = strs.find(to_str, offset_start) if (offset_end := strs.find(to_str, offset_start)) != -1 else len(strs)
    return strs[offset_start:offset_end]

def format_strtime(time, suff={}):
    h, remainder = divmod(time, 3600)
    m, s = divmod(remainder, 60)
    return ' '.join(f"{val}{unit}" for val, unit in ((h, suff.get('h', 'H')), (m, suff.get('m', 'M')), (s, suff.get('s', 'sec'))) if val)

def format_time(strtime):
    match = re.fullmatch(r'(\d+)(sec|min|h|d)', strtime)
    if match:
        value, unit = match.groups()
        value = int(value)
        return value if unit == 'sec' else value * 60 if unit == 'min' else value * 3600 if unit == 'h' else value * 86400
    return 0

def file_get_contents(filename):
    try: return open(filename, 'r', newline='', encoding='utf-8').read()
    except FileNotFoundError: return ''
    
def file_put_contents(filename, content, mode='w'):
    try: open(filename, mode, newline='', encoding='utf-8').write(content); return len (content)
    except IOError: return False

async def get_data(url, proxy=''):
    buffer = BytesIO()
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    params = {
        'url': url,
        'proxy': proxy,
        'buffer': buffer,
        'headers': curl_headers(headers)
    }
    c = curl_setup(params)

    try:
        c.perform()
    except pycurl.error as e:
        return f'Error: {e}'
    finally:
        c.close()

    return buffer.getvalue().decode('utf-8')

def curl_headers(custom_headers={}):
    default_headers = {
        'User-Agent': custom_headers.get('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko'),
        'Accept': custom_headers.get('Accept', '*/*'),
        'Accept-Language': custom_headers.get('Accept-Language', 'en-US,en;q=0.5'),
        'Upgrade-Insecure-Requests': custom_headers.get('Upgrade-Insecure-Requests', '1'),
        'Sec-Fetch-Dest': custom_headers.get('Sec-Fetch-Dest', 'document'),
        'Sec-Fetch-Mode': custom_headers.get('Sec-Fetch-Mode', 'navigate'),
        'Sec-Fetch-Site': custom_headers.get('Sec-Fetch-Site', 'same-origin'),
        'Sec-Fetch-User': custom_headers.get('Sec-Fetch-User', '?1'),
        'Priority': custom_headers.get('Priority', 'u=1')
    }

    for key, value in custom_headers.items():
        if key not in default_headers:
            default_headers[key] = value

    return [f'{key}: {value}' for key, value in default_headers.items()]

def curl_setup(params):
    c = pycurl.Curl()
    c.setopt(c.SSL_VERIFYHOST, 2)
    c.setopt(c.SSL_VERIFYPEER, 0)
    c.setopt(c.URL, params.get('url'))
    c.setopt(c.CAINFO, certifi.where())
    c.setopt(c.PROXY, params.get('proxy', ''))
    c.setopt(c.WRITEDATA, params.get('buffer'))
    c.setopt(c.ACCEPT_ENCODING, 'gzip, deflate')
    c.setopt(c.HTTPHEADER, params.get('headers', []))
    cookie_file = f"{COOKIE_DIR}{gstrb('//', '/', params.get('url'))}.txt"
    c.setopt(c.COOKIEJAR, cookie_file)
    c.setopt(c.COOKIEFILE, cookie_file)
    if params.get('postfields'):
        c.setopt(c.POSTFIELDS, params.get('postfields'))
    return c
