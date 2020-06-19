import logging
from os import getenv
from time import sleep

from dotenv import load_dotenv
from requests import post

load_dotenv()
logging.basicConfig(filename='access.log', level=logging.INFO, format='%(asctime)s: %(message)s',
                    datefmt='%a %d-%b-%Y %H:%M:%S')

url = 'http://nas.ub.ac.id/ac_portal/login.php'
interval = getenv('NAS_INTERVAL')
data = {'opr': 'pwdLogin',
        'userName': getenv('NAS_USERNAME'),
        'pwd': getenv('NAS_PASSWORD'),
        'rememberPwd': '0'
        }

while True:
    res = post(url, data=data).content.decode('utf-8')

    logging.info(res)
    sleep(int(interval) * 60)
