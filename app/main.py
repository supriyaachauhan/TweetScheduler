from flask import Flask, render_template, request, redirect
import gspread
from datetime import datetime, timezone
# to run server : flask --app main(app name) run  

app = Flask(__name__)

gc = gspread.service_account(filename='C:/Users/dipender/Desktop/auto-tweet/credentials.json')

sh = gc.open_by_key('1ire7GxCHsAbyO-Zp_ReLNPSaCwBKiBA05PUU7ioH0F4')

worksheet = sh.sheet1

class Tweet():
    def __init__(self, time, message, done, row_idx):
        self.time = time
        self.message = message
        self.done = done
        self.row_idx = row_idx

@app.route('/')
def tweet_list():

    tweet_records = worksheet.get_all_records()
    print("tweet_records",tweet_records)

    tweets = []
    for idx, data in enumerate(tweet_records, start=2):
        tweet = Tweet(**data, row_idx=idx)
        tweets.append(tweet)

    n_open_tweets = sum(1 for tweet in tweets if not tweet.done)
    return render_template('base.html', tweets=tweets, n_open_tweets=n_open_tweets)

    # return 'Hello world'

# def get_date_time(date_time_str):
#     date_time_obj = None
#     error_code = None

#     try:
#         date_time_obj = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S" )
#     except ValueError as e:
#         error_code = f'Error! {e}'


@app.route('/tweet', methods=['POST'])
def add_tweets():

    tweet = request.form['tweet']
    if not tweet:
        return "error! no tweet"
    date_time_str = request.form['time']
    if not date_time_str:
        return "error! no time"
    password = request.form['password']
    if not password or password != '123':
        return "error! wrong password"
    
    if len(tweet) > 280:
        return "error! message too long!"
    
    try:
        date_time_obj = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S" )
    except ValueError as e:
        print("error in date--", e)
        return f'Error! {e}'
    
    save_tweet = [str(date_time_obj), tweet, 0]
    worksheet.append_row(save_tweet)

    return redirect('/')

@app.route('/delete/<int:row_idx>')
def delete_tweet(row_idx):
    worksheet.delete_rows(row_idx)
    return redirect('/')