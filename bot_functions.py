import json
import os
import requests
import sys
from pathlib import Path
from random import randint

import clearbit
import django
from dotenv import load_dotenv

from customuser.models import User, Post

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialbook.settings')
try:
    from django.core.management import execute_from_command_line
except ImportError as exc:
    raise ImportError(
        "Couldn't import Django"
    ) from exc
execute_from_command_line(sys.argv)

django.setup()


def signup(server, api, number_of_users):
    for x in range(number_of_users):
        user = "korisnik" + str(x)
        email = user + "@gmail.com"
        password = "lozinka" + str(x)

        r = requests.post(server + "customuser/api/signup/",
                          data={'username': user, 'email': email, 'password1': password, 'password2': password,
                                'givenName': "", 'familyName': ""},
                          headers={'Authorization': "Bearer " + api})
        r = r.json()
        print(r)
    print(str(number_of_users) + " Users created!")


def create_posts(server, api, max_posts_per_user, number_of_users):
    count = 0
    for x in range(number_of_users):
        user = "korisnik" + str(x)
        posts_user = randint(1, max_posts_per_user)

        for y in range(posts_user):
            post = "tekstU" + str(x) + "P" + str(y)
            r = requests.post(server + "customuser/api/post/", data={'user': user, 'post_text': post},
                              headers={'Authorization': "Bearer " + api})
            r = r.json()
            count = count + 1
        print(str(posts_user) + " Posts created for user" + user)
    print(str(count) + " Posts created in total!")


def like_posts(server, api, number_of_users, max_likes_per_user):
    user_list = User.objects.order_by("-posts")
    usercount = user_list.count()
    for x in range(0, usercount - 1):
        nrlikes = 0
        while user_list[x].likes < max_likes_per_user:
            posts = Post.objects.exclude(user=user_list[x].id).order_by("likes")
            if posts[0].likes != 0:
                break

            toLikeUser = posts[0].user
            toLikeUserPosts = User.objects.get(username=toLikeUser).posts
            likingUser = user_list[x].username
            user = toLikeUser
            post = randint(1, toLikeUserPosts)

            r = requests.post(server + "customuser/api/like/",
                              data={'likingUser': likingUser, 'upvote': "True", 'user': user, 'post': str(post)},
                              headers={'Authorization': "Bearer " + api})
            user_list[x].likes += 1
            nrlikes += 1
        print("user " + str(x) + " made " + str(nrlikes) + "likes!")


def token_request():
    server = input("Write Django development server address. Leave blank if it is: http://127.0.0.1:8000/ ")
    if server == "":
        server = "http://127.0.0.1:8000/"

    email = input("Enter superuser email: ")
    password = input("Enter superuser password: ")
    r = requests.post(server + "api/token/", data={'email': email, 'password': password})
    r = r.json()
    access = r["access"]

    with open("bot.config", "r+") as f:
        data = json.load(f)
        data["host"] = server
        data["token"] = access
        data["su"] = email
        data["pass"] = password

        f.seek(0, 0)
        json.dump(data, f)

    print("\nJWT authentication token. Lasts for 2 hours before need for refresh.")


def bot_configuration():
    print("\nNow, you will be asked to setup configuration for bot activities. \n")
    number_of_users = input("How many customuser you wish to create: ")
    max_posts_per_user = input("Maximum number of posts per user: ")
    max_likes_per_user = input("Maximum number of likes per user: ")

    with open("bot.config", "r+") as f:
        data = json.load(f)

        data["number_of_users"] = number_of_users
        data["max_posts_per_user"] = max_posts_per_user
        data["max_likes_per_user"] = max_likes_per_user

        f.seek(0, 0)
        json.dump(data, f)

    print("\nbot.config updated!")


def bot_activity():
    data = ""
    with open("bot.config", "r+") as f:
        data = json.load(f)

    server = data["host"]
    api = data["token"]
    number_of_users = int(data["number_of_users"])
    max_posts_per_user = int(data["max_posts_per_user"])
    max_likes_per_user = int(data["max_likes_per_user"])

    signup(server, api, number_of_users)
    create_posts(server, api, max_posts_per_user, number_of_users)

def clearbit():
    env_path = Path('socialbook') / '.env'
    load_dotenv(dotenv_path=env_path, verbose=True)
    clearbit.key = os.environ["CLEARBIT"]

    email = input("Type in email you want additional public data for: ")
    lookup = clearbit.Enrichment.find(email=email, stream=True)

    if lookup != None:
        print('Email found!')
        print(lookup)
    else:
        print('Email not found')
        return ["null", "null"]


def emailhunter():
    env_path = Path('socialbook') / '.env'
    load_dotenv(dotenv_path=env_path, verbose=True)
    email = input("Type in email you want to check legitimity: ")
    key = os.environ["EMAILHUNTER"]
    req = {"api_key": key, "email": email}
    odg = requests.get("https://api.hunter.io/v2/email-verifier", params=req)
    data = odg.json()
    data = data["data"]
    print(data)
