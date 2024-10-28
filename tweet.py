from os import environ
import gspread
import tweepy
import time
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta

load_dotenv()
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_TOKEN = environ['ACCESS_TOKEN']
ACCESS_SECRET = environ['ACCESS_SECRET']


auth = tweepy.OAuth1UserHandler(
    CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET
)

api = tweepy.API(auth)

gc = gspread.service_account(filename='credentials.json')

sh = gc.open_by_key('1ire7GxCHsAbyO-Zp_ReLNPSaCwBKiBA05PUU7ioH0F4')

worksheet = sh.sheet1

INTERVAL = int(environ['INTERVAL'])
DEBUG = environ['DEBUG'] == '1'

def main():
    while True:
        print('hello tweet')
        tweet_records = worksheet.get_all_records()

        current_time_obj = datetime.now(timezone.utc) - timedelta(hours=2)

        # logger.info(f'{len(tweet_records)} tweets found at {now_time_cet.date()}')
        # time.sleep(INTERVAL)

        for idx, data in enumerate(tweet_records, start=2):
            msg = data['message']
            time_str = data['time']
            done = data['done']

            date_time_obj = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S" )
            print("date_time_obj ---->>", date_time_obj)

            if not done:

                now_time_cet = datetime.now(timezone.utc) - timedelta(hours=2)
                formatted_now_time_cet = now_time_cet.strftime("%Y-%m-%d %H:%M:%S")
                now_time_cet_obj = datetime.strptime(formatted_now_time_cet, "%Y-%m-%d %H:%M:%S")

                if date_time_obj > now_time_cet_obj:
                    logger.info('this should be tweeted')
                    try:
                        api.update_status(msg)
                        worksheet.update_cell(idx,3,1)   # column 3 with value 1

                    except Exception as e:
                        logger.error(f'error is {e}')
        


        time.sleep(INTERVAL)


if __name__ == '__main__':
    main()