import sqlite3

from Report.reportBots import reportBots
from Report.reportEmptyUsers import reportEmptyUsers


def reportUsers(TARGET_USER, twitter_api):
    limit = twitter_api.rate_limit_status()["resources"]['users']['/users/report_spam']
    limitSpam = int(limit["remaining"])
    print("Remaining rate (Spam): " + limitSpam.__str__())

    if limitSpam > 0:
        print("Reporting bots")
        reportBots(TARGET_USER, twitter_api, 0.95)
        limit = twitter_api.CheckRateLimit("https://api.twitter.com/1.1/users/report_spam.json")
        limitSpam = int(limit[1])
    if limitSpam > 0:
        print("Remaining rate (Spam, after reporting bots): " + limitSpam.__str__())
        print("Reporting empty users")
        reportEmptyUsers(TARGET_USER, twitter_api)
