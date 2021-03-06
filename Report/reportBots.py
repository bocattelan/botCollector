from datetime import datetime, timezone

import tweepy
from utils.config import conn


def reportBots(TARGET_USER, twitter_api, probabilityCut):
    c = conn.cursor()

    users = c.execute(
        'SELECT * FROM {} WHERE capUniversal >= ? AND (reported IS NULL AND (lastCheck!=0 or lastCheck IS NULL))'.format(
            TARGET_USER), (probabilityCut,)).fetchall()
    print("Collected " + len(users).__str__() + " possible bots")
    for user in users:
        reportBot(TARGET_USER, twitter_api, user)


def reportBot(TARGET_USER, twitter_api, user):
    c = conn.cursor()
    try:
        twitter_api.report_spam(user_id=user[0])
        c.execute("UPDATE {} SET reported = ?, lastCheck = ? WHERE userId = ? AND userName = ?".format(TARGET_USER),
                  (1, datetime.now(timezone.utc).ctime(), user[0], user[1],))
        conn.commit()
        print("Reported user " + user[1] + " with probability " + user[3].__str__())
    except tweepy.TweepError as error:
        if error.__str__() == "[{'code': 205, 'message': 'You are over the limit for spam reports.'}]":
            print("Spam reporting limit reached")
            return 205
        else:
            print("Else: " + error.__str__())
