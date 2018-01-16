import tweepy
import os
import re
import CommentParser
import sys
import subprocess
import yaml
import json


def tweet(html_file, post_url, image_url):
    config_file = os.path.expanduser('~/.tweeter')
    if not os.path.exists(config_file):
        print('~/.tweeter file is missing')
        print('Create that and add all the config values in it')
        sys.exit()

    # Read the config file
    with open(config_file) as file:
        config = yaml.load(file)

    consumer_key = config["consumer_key"]
    consumer_secret = config["consumer_secret"]
    access_token = config["access_token"]
    access_token_secret = config["access_token_secret"]

    # Using the keys, setup the authorization
    authorization = tweepy.OAuthHandler(consumer_key, consumer_secret)
    authorization.set_access_token(access_token, access_token_secret)
    # Create the API object
    twitter = tweepy.API(authorization)

    with open(html_file) as file:
        html_file_contents = file.read()

    # Read file and extract the comments
    re_comments = re.compile('\s*<!--(.*)-->', re.DOTALL)
    comments_text = re_comments.search(html_file_contents).group(1).strip()
    comments_parser = CommentParser.parse_comments(comments_text)
    # print(len(comments_parser.labels), flush=True)

    lines = (
        f'Day {get_days_since_challenge_started()} of #30DaysOfBlogging challenge',
        comments_parser.title,
        " ",
        "#FreBlogg " + get_labels_as_hash_tags(comments_parser.labels),
        f"{post_url}",
    )

    generated_tweet = "\n".join(lines)
    tweet_file = html_file[:-5] + ".tweet"

    with open(tweet_file, 'w') as file:
        file.write(generated_tweet)

    # Start vim with the markdown file open on line #10
    subprocess.run(['gvim', '+3', tweet_file])

    # Read the file
    with open(tweet_file) as file:
        full_tweet = file.read()

    # If image file is given
    if image_url:
        t = twitter.update_with_media(image_url, full_tweet)
    else:
        # Text Tweet
        t = twitter.update_status(full_tweet)

    print(str(t).encode())

    # Media Tweet
    # image = os.environ['USERPROFILE'] + "\\Pictures\\cubes.jpg"
    # twitter.update_with_media(image, "Tweet with media using #tweepy")


def get_labels_as_hash_tags(labels):
    if labels:
        return "#" + " #".join(labels)

    # If there are no labels, then return empty string
    return ""


def get_days_since_challenge_started():
    from datetime import date
    start = date(2017, 12, 23)
    today = date.today()
    return (today - start).days + 1  # adding 1 as the 23rd December was Day #1 and not Day #0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: tweeter <html-file> <article-link> ")
        sys.exit()

    html_file = sys.argv[1]
    post_url = sys.argv[2]
    image_url = None

    # If image is also given
    if len(sys.argv) == 4:
        image_url = sys.argv[3]

    tweet(html_file, post_url, image_url)
