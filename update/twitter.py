def update_twitter(twitter_api, messages):
    for message in messages:
        response = twitter_api.update_with_media(filename=message["media"], status=message["status"], )
        print("Update status: " + response.__str__())
