import sqlite3
import subprocess
from datetime import datetime

import botometer
import tweepy
from twitter import TwitterError
import twitter

if __name__ == '__main__':
    while True:
        try:
            iteration = 0
            # user being studied
            TARGET_USER = "jairbolsonaro"

            conn = sqlite3.connect('data/database.db')
            c = conn.cursor()
            try:
                c.execute(
                    '''CREATE TABLE {} (userId integer, userName text, capEnglish real, capUniversal real)'''.format(
                        TARGET_USER))
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
            }

            next_cursor = -1
            while True:
                print("Starting Twitter API")
                api = twitter.Api(consumer_key=CONSUMER_KEY,
                                  consumer_secret=CONSUMER_SECRET,
                                  sleep_on_rate_limit=True,
                                  application_only_auth=True)
                print("Starting Botometer API")
                bom = botometer.Botometer(wait_on_ratelimit=True,
                                          mashape_key=mashape_key,
                                          **twitter_app_auth)

                # create plots and update git server
                if iteration == 10:
                    subprocess.call(["bash", "update.sh"])
                    iteration = 0
                iteration = iteration + 1

                limit = api.CheckRateLimit("https://api.twitter.com/1.1/followers/list.json")
                print("Next rate reset (Twitter):" + datetime.utcfromtimestamp(limit[2]).strftime('%Y-%m-%d %H:%M:%S'))
                conn.commit()
                try:
                    next_cursor, previous_cursor, followers = api.GetFollowersPaged(screen_name=TARGET_USER,
                                                                                    cursor=next_cursor)
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
                        print("Checking " + follower.AsDict()["screen_name"] + " counter: " + counter.__str__())
                        counter = counter + 1
                        # check if it already exists
                        c.execute('SELECT * FROM {} WHERE userId=?'.format(TARGET_USER),
                                  (follower.AsDict()["id"],))
                        if c.fetchone() is not None:
                            continue
                        result = bom.check_account(follower.AsDict()["id"])
                        # store user data
                        c.execute('INSERT INTO {} VALUES (?,?,?,?)'.format(TARGET_USER),
                                  [result["user"]["id_str"], result["user"]["screen_name"], result["cap"]["english"],
                                   result["cap"]["universal"]])
                    except botometer.NoTimelineError as error:
                        # some accounts have no timeline, so botometer cannot score them
                        c.execute('INSERT INTO {} VALUES (?,?,?,?)'.format(TARGET_USER),
                                  [follower.AsDict()["id"], follower.AsDict()["screen_name"],
                                   -1, -1])
                    except tweepy.TweepError:
                        # some accounts have protected tweets, so botometer cannot score them
                        c.execute('INSERT INTO {} VALUES (?,?,?,?)'.format(TARGET_USER),
                                  [follower.AsDict()["id"], follower.AsDict()["screen_name"],
                                   -2, -2])
                    except Exception as error:
                        print("Default behavior for error: " + error.__str__())
                        conn.commit()
        except Exception as error:
            print("Uncaught exception: " + error.__str__())
