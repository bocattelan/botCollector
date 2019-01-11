import sqlite3
import time

import tweepy


# Due to limitations from twitter, can only report 20 accounts before having to wait
def reportEmptyUsers(TARGET_USER, twitter_api, amountToReport):
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    # Get all users where the universal score is -1 (no timeline) and was not reported (NULL)
    # also filter out accounts known to have been deleted
    users = c.execute(
        'SELECT * FROM {} WHERE capUniversal=-1 AND (reported IS NULL AND (lastCheck!=0 or lastCheck IS NULL))'.format(
            TARGET_USER)).fetchmany(amountToReport)

    for user in users:
        try:
            # userTest = twitter_api.get_user(screen_name=user[1])
            twitter_api.report_spam(user_id=user[0])
            c.execute("UPDATE {} SET reported = ?, lastCheck = ? WHERE userId = ? AND userName = ?".format(TARGET_USER),
                      (1, time.time(), user[0], user[1],))
            conn.commit()
            print("Reported user " + user[1] + " successfully")
        except tweepy.TweepError as error:
            if error.__str__() == "[{'code': 205, 'message': 'You are over the limit for spam reports.'}]":
                print("Spam reporting limit reached")
                # wait 30 minutes
                return 205
            else:
                print("Else: " + error.__str__())
