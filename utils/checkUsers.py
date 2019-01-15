import calendar
import time
from datetime import datetime, timezone
import botometer
import tweepy
from dateutil.tz import tzlocal

from utils import config
from Report.reportBots import reportBot


# TODO add user creation date
def checkUser(TARGET_USER, bom_api, user):
    user_id = user.id_str
    user_name = user.screen_name
    created_at = user.created_at
    location = user.location
    lang = user.lang
    favorites_count = user.favourites_count
    followers_count = user.followers_count
    listed_count = user.listed_count
    friends_count = user.friends_count
    statuses_count = user.statuses_count

    user_info = [created_at, location, lang, favorites_count, followers_count, listed_count, friends_count, statuses_count]

    c = config.conn.cursor()
    try:
        print("Checking " + user_name)
        # check if it already exists
        c.execute('SELECT * FROM {} WHERE userId=?'.format(TARGET_USER),
                  (user_id,))
        if c.execute("SELECT EXISTS(SELECT 1 FROM {} WHERE userId=?)".format(TARGET_USER),
                     [user_id]).fetchone()[0] == 1:
            print("User already exists: " + user_name)
            return
        # TODO change to check_accounts_in
        result = bom_api.check_account(user_id)
        # store user data
        # TODO add location, lang, favorites countm followers count, listed count,friends count, statuses count,
        c.execute('INSERT INTO {} VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)'.format(TARGET_USER),
                  [user_id, user_name, result["cap"]["english"],
                   result["cap"]["universal"], 0, datetime.now(timezone.utc).ctime()] + user_info)

        if float(result["cap"]["universal"]) >= 0.9:
            limit = bom_api.twitter_api.rate_limit_status()["resources"]['users']['/users/report_spam']
            limitSpam = int(limit["remaining"])
            print(
                "Remaining rate (Spam): " + limitSpam.__str__() + " which resets at " +
                datetime.fromtimestamp(limit["reset"], tzlocal()).strftime('%Y-%m-%d %H:%M:%S'))
            possibleBot = [user_id, user_name,
                           result["cap"]["english"], result["cap"]["universal"]]
            reportBot(TARGET_USER, bom_api.twitter_api, possibleBot)
    except botometer.NoTimelineError:
        print("No timeline")
        # some accounts have no timeline, so botometer cannot score them - still suspicious
        c.execute('INSERT INTO {} VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)'.format(TARGET_USER),
                  [user_id, user_name,
                   -1, -1, 0, datetime.now(timezone.utc).ctime()] + user_info)
    except tweepy.TweepError:
        print("Waiting for possible server error")
        time.sleep(10)
    except Exception as error:
        print("Default behavior for error: " + error.__str__())
