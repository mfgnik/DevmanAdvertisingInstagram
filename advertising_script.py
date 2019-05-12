import instabot
import os
from dotenv import load_dotenv
import re
from argparse import ArgumentParser
from random import choice


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        '--url_path',
        help='path to the instagram photo',
        required=True
    )
    parser.add_argument(
        '--username',
        help='username of account',
        required=True
    )
    return parser.parse_args()


def is_user_exists(bot, username):
    return bot.get_user_id_from_username(username) is not None


def check_comment(bot, comment, likers, followers):
    # Regexp was found on this site https://blog.jstassen.com/2016/03/code-regex-for-instagram-username-and-hashtags/
    regexp = r'(?:@)([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)'
    users = re.findall(regexp, comment['text'])
    any_users_exists = any(is_user_exists(bot, user) for user in users)
    user_id = comment['user_id']
    return any_users_exists and user_id in followers and user_id in likers


def check_comments(bot, url_path, username):
    media_id = bot.get_media_id_from_link(url_path)
    comments = bot.get_media_comments_all(media_id)
    likers = set(bot.get_media_likers(media_id))
    followers = set(bot.get_user_followers(bot.get_user_id_from_username(username)))
    return set(comment['username'] for comment in comments if check_comment(bot, comment, likers, followers))


if __name__ == '__main__':
    load_dotenv()
    arguments = parse_args()
    bot = instabot.Bot()
    bot.login(username=os.getenv('login'), password=os.getenv('password'))
    appropriate_comments = check_comments(bot, arguments.url_path, arguments.username)
    winner = choice(appropriate_comments)
    print(winner)

