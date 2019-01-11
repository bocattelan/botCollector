import os
import sqlite3
import subprocess
import time
from datetime import datetime

import botometer
import tweepy
from dateutil.tz import tzlocal
from twitter import TwitterError
import twitter

from Report.reportUsers import reportUsers
from checkIfExists import checkIfExists
from Report.reportBots import reportBots, reportBot
from Report.reportEmptyUsers import reportEmptyUsers
from checkUsers import checkUser

if __name__ == '__main__':
    if not os.path.exists("data/"):
        os.makedirs("data/")

    while True:
        try:
            iteration = 0
            # user being studied
            TARGET_USER = "jairbolsonaro"

            conn = sqlite3.connect('data/database.db')
            c = conn.cursor()
            try:
                c.execute(
                    '''CREATE TABLE {} (userId integer, userName text, capEnglish real, capUniversal real, reported 
                    integer, lastCheck integer)'''.format(
                        TARGET_USER))
                conn.commit()
            except Exception as error:
                print("Table Exception: " + error.__str__())

            # create twitter api object, using the tokens from a file called tokens.conf inside the data folder
            tokenFile = open("data/tokens.conf", "r")
            CONSUMER_KEY = tokenFile.readline().__str__().rstrip('\n')
            CONSUMER_SECRET = tokenFile.readline().__str__().rstrip('\n')
            ACCESS_TOKEN_KEY = tokenFile.readline().__str__().rstrip('\n')
            ACCESS_TOKEN_SECRET = tokenFile.readline().__str__().rstrip('\n')

            mashape_key = tokenFile.readline().__str__().rstrip('\n')
            twitter_app_auth = {
                'consumer_key': CONSUMER_KEY,
                'consumer_secret': CONSUMER_SECRET,
                'access_token': ACCESS_TOKEN_KEY,
                'access_token_secret': ACCESS_TOKEN_SECRET
            }

            next_cursor = -1
            while True:
                print("Starting Twitter API")
                api = twitter.Api(consumer_key=CONSUMER_KEY,
                                  consumer_secret=CONSUMER_SECRET,
                                  access_token_key=ACCESS_TOKEN_KEY,
                                  access_token_secret=ACCESS_TOKEN_SECRET,
                                  sleep_on_rate_limit=True,
                                  application_only_auth=True)
                print("Starting Botometer API")
                bom = botometer.Botometer(wait_on_ratelimit=True,
                                          mashape_key=mashape_key,
                                          **twitter_app_auth)
                bom.twitter_api.wait_on_rate_limit_notify = True

                conn = sqlite3.connect('data/database.db')
                c = conn.cursor()
                # create plots and update git server
                if iteration == 5:
                    # Check saved accounts for deleted ones
                    checkIfExists(TARGET_USER, bom.twitter_api)
                    subprocess.call(["bash", "update.sh"])
                    time.sleep(2)
                    iteration = 0
                iteration = iteration + 1
                limit = api.CheckRateLimit("https://api.twitter.com/1.1/followers/list.json")
                print("Next rate reset (Followers): " + datetime.fromtimestamp(limit[2], tzlocal()).strftime(
                    '%Y-%m-%d %H:%M:%S'))

                # reportUsers(TARGET_USER, bom.twitter_api)
                conn.commit()

                try:
                    next_cursor, previous_cursor, followers = api.GetFollowersPaged(screen_name=TARGET_USER,
                                                                                    cursor=next_cursor,
                                                                                    include_user_entities=True,
                                                                                    skip_status=True)
                    print("Got followers")
                except TwitterError as error:
                    print("Could not get followers: " + error.__str__())
                    continue
                if len(followers) == 0:
                    print("No more followers!")
                    api.ClearCredentials()
                    c.close()
                    exit(0)

                for follower in followers:
                    checkUser(TARGET_USER, bom, follower.id, follower.screen_name, conn)
                conn.commit()
                reportEmptyUsers(TARGET_USER, bom.twitter_api, 1)
        except Exception as error:
            print("Uncaught exception: " + error.__str__())
