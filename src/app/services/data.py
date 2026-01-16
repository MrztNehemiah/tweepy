import json


def tweet_data(data) -> list:
    list_data = []
    with open(data, "r") as tweets:
        tweets_json = json.load(tweets)

        for item in range(len(tweets_json)):
            list_data.append(tweets_json[item]["tweet"]["full_text"])

    return list_data
