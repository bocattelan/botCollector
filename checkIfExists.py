import sqlite3
import time

import tweepy


def checkIfExists(TARGET_USER, twitter_api):
    conn = sqlite3.connect('data/database.db')
    c = conn.cursor()
    print("Testing if users still exist")
    usersAll = c.execute(
        'SELECT userId FROM {} WHERE (lastCheck!=0 or lastCheck IS NULL)'.format(
            TARGET_USER)).fetchall()
    while len(usersAll) != 0:
        try:
            users = []
            print("Users left: " + len(usersAll).__str__())
            for i in range(100):
                if len(usersAll) == 0:
                    break
                users.append(usersAll.pop())
            userIds = [item[0] for item in users]
            userResponse = twitter_api.lookup_users(user_ids=userIds, include_entities=False)
            userInResponse = [item["id"] for item in userResponse]
            requestTime = time.time()
            for userId in userIds:
                # Check if this id is in the response
                if userId in userInResponse:
                    c.execute(
                        "UPDATE {} SET lastCheck = ? WHERE userId = ?".format(TARGET_USER),
                        [requestTime, userId])
                else:
                    c.execute(
                        "UPDATE {} SET lastCheck = 0 WHERE userId = ?".format(TARGET_USER),
                        [userId])
                    userName = c.execute('SELECT userName FROM {} WHERE userId = ?'.format(
                        TARGET_USER), [userId]).fetchone()
                    print("Account removed: " + userName[0])
            conn.commit()
        except Exception as error:
            print("Error: " + error.__str__())
