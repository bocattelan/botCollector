def update_twitter(twitter_api, message):
    response = twitter_api.update_status(message)
    print("Update status: " + response.__str__())
