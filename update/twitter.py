def update_twitter(twitter_api):
    twitter_payload = "Hallo!"
    response = twitter_api.update_status(twitter_payload)
    print("Update status: " + response)
