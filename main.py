import json
import logging
import time
from datetime import datetime
from os import getenv

import schedule
from dotenv import load_dotenv
from requests import post
from requests.exceptions import RequestException


def login(log_to_file=False, print_message=True):
    time_format = '%a %d-%b-%Y %H:%M:%S'

    if log_to_file:
        logging.basicConfig(filename='access.log', level=logging.INFO, format='%(asctime)s: %(message)s',
                            datefmt=time_format)

    load_dotenv()

    url = 'http://nas.ub.ac.id/ac_portal/login.php'
    data = {'opr': 'pwdLogin',
            'userName': getenv('NAS_USERNAME'),
            'pwd': getenv('NAS_PASSWORD'),
            'rememberPwd': '0'
            }

    try:
        res = post(url, data=data).content.decode('utf-8').replace("'", '"')
    except RequestException as err:
        print(err)
    else:
        res_json = json.loads(res)
        now = datetime.now().strftime(time_format)

        if print_message:
            print(now, 'Success:' if res_json['success'] else 'Failure:', res_json['msg'])

        if log_to_file:
            logging.info(res)


def main():
    load_dotenv()

    interval = int(getenv('NAS_INTERVAL'))

    schedule.every(interval).minutes.do(login)
    print(f'Logging in every {interval} minutes...')
    login()

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
