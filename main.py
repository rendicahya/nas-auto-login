import json
import logging
import time
from os import getenv

import schedule
from dotenv import load_dotenv
from requests import post
from requests.exceptions import RequestException


def login():
    load_dotenv()
    logging.basicConfig(level=logging.INFO, format='%(levelname)s %(asctime)s: %(message)s')

    url = 'http://nas.ub.ac.id/ac_portal/login.php'
    data = {
        'opr': 'pwdLogin',
        'userName': getenv('NAS_USERNAME'),
        'pwd': getenv('NAS_PASSWORD'),
        'rememberPwd': '0'
    }

    try:
        resp = post(url, data=data)
    except RequestException as e:
        logging.error('Failed logging in')
    else:
        if resp.status_code == 200:
            resp_str = resp.content.decode('utf-8').replace("'", '"')
            resp_json = json.loads(resp_str)

            logging.info('Success:' if resp_json['success'] else 'Failure:', resp_json['msg'])


def main():
    load_dotenv()

    interval = int(getenv('NAS_INTERVAL', default=5))

    schedule.every(interval).minutes.do(login)
    logging.info(f'Logging in every {interval} minutes...')
    login()

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
