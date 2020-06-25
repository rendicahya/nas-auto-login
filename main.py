import json
import logging
from datetime import datetime
from os import getenv
from time import sleep

from dotenv import load_dotenv
from requests import post

time_format = '%a %d-%b-%Y %H:%M:%S'

load_dotenv()
logging.basicConfig(filename='access.log', level=logging.INFO, format='%(asctime)s: %(message)s',
                    datefmt=time_format)

url = 'http://nas.ub.ac.id/ac_portal/login.php'
interval = getenv('NAS_INTERVAL')
data = {'opr': 'pwdLogin',
        'userName': getenv('NAS_USERNAME'),
        'pwd': getenv('NAS_PASSWORD'),
        'rememberPwd': '0'
        }

while True:
    res = post(url, data=data).content.decode('utf-8').replace("'", '"')
    res_json = json.loads(res)
    now = datetime.now().strftime(time_format)

    print(now, 'Success:' if res_json['success'] else 'Failure:', res_json['msg'])
    logging.info(res)
    sleep(int(interval) * 60)
