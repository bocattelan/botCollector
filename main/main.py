import os
import sqlite3
import time
from datetime import datetime

import botometer
from dateutil.tz import tzlocal
from twitter import TwitterError
import twitter

from update.twitter import update_twitter
from utils.checkIfExists import checkIfExists
from Report.reportEmptyUsers import reportEmptyUsers
from utils.checkUsers import checkUser
from plots.generatePlots import generate_plot
from utils.config import conn
from utils.config import MAIN_DIRECTORY
from itertools import cycle

if __name__ == '__main__':
    if not os.path.exists(MAIN_DIRECTORY + "/data/"):
        os.makedirs(MAIN_DIRECTORY + "/data/")
    TARGET_USERs = ["jairbolsonaro", "xuxameneghel", "CarlosBolsonaro", "leandroruschel", "cnn"]
    userPool = cycle(TARGET_USERs)
    cursors = {key: -1 for (key) in TARGET_USERs}
    for TARGET_USER in userPool:
        try:
            c = conn.cursor()
            try:
                # [created_at, location, lang, favorites_count, followers_count, listed_count, friends_count,
                # statuses_count]
                c.execute(
                    '''CREATE TABLE {} (userId text, userName text, capEnglish real, capUniversal real, reported 
                    integer, lastCheck text, createdAt text, location text, language text, favoritesCount integer, 
                    followersCount integer, listedCount integer, friendsCount integer, statusesCount 
                    integer)'''.format(
                        TARGET_USER))
                conn.commit()
                print("Created table " + TARGET_USER)
            except Exception as error:
                print("Table Exception: " + error.__str__())

            # create twitter api object, using the tokens from a file called tokens.conf inside the data folder
            if not os.path.isfile(MAIN_DIRECTORY + "/data/tokens.conf"):
                print("You need a token file with the following tokens (in order):")
                print("CONSUMER KEY (twitter)")
                print("CONSUMER SECRET (twitter)")
                print("ACCESS KEY (twitter)")
                print("ACCESS TOKEN (twitter)")
                print("MASHAPE KEY (botometer)")
                exit(-1)
            tokenFile = open(MAIN_DIRECTORY + "/data/tokens.conf", "r")

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

            next_cursor = cursors[TARGET_USER]

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

            #update_twitter(bom.twitter_api)

            conn = sqlite3.connect(MAIN_DIRECTORY + '/data/database.db')
            c = conn.cursor()

            # create plots and update git server
            # Check saved accounts for deleted ones
            checkIfExists(TARGET_USER, bom.twitter_api)
            # TODO use a separate process with gitpython
            # subprocess.call(["bash", "update.sh"])
            generate_plot(TARGET_USER)
            limit = api.CheckRateLimit("https://api.twitter.com/1.1/followers/list.json")
            print("Next rate reset (Followers): " + datetime.fromtimestamp(limit[2], tzlocal()).strftime(
                '%Y-%m-%d %H:%M:%S'))
            conn.commit()

            try:
                cursors[TARGET_USER], previous_cursor, followers = api.GetFollowersPaged(screen_name=TARGET_USER,
                                                                                         cursor=next_cursor,
                                                                                         include_user_entities=False,
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
            counter = 1
            for follower in followers:
                try:

                    checkUser(TARGET_USER, bom, follower)
                except Exception as error:
                    print("Failed to check " + follower.screen_name)
                    print("Unexpected error: " + error.__str__())
                counter = counter + 1
                if (counter % 20) == 0:
                    print("Checked " + counter.__str__() + " users")
            conn.commit()
            reportEmptyUsers(TARGET_USER, bom.twitter_api, 1)
        except Exception as error:
            print("Uncaught exception: " + error.__str__())
