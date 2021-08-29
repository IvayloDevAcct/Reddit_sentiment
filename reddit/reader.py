from requests import auth
from requests import post
from requests import get
import json


with open("C:\\Users\\ivayl\\Documents\\Nexo Work\\creds.json", "r", encoding="utf8") as f:
    creds = json.load(f)

"""This module was created before I discovered the praw library. It is not in use, except for the credentials"""


# class RedditReader:
#     def __init__(self):
#         self.__token = self.login()
#
#     def login(self):
#         """Authenticates my Reddit user account and creates headers for future API requests
#         :returns list"""
#
#         authorization = auth.HTTPBasicAuth("4o3BOo3lnIC4dPi5KSA8Jw", creds["secred"])
#         # Set request parameters
#         data = {
#             'grant_type': "password",
#             "username": "ivailo_opalchenski",
#             "password": creds["pass"]
#         }
#         headers = {'User-Agent': "Version 1"}
#
#         token_request = post("https://www.reddit.com/api/v1/access_token", auth=authorization,
#                              data=data, headers=headers).json()
#
#         headers["Authorization"] = f"bearer {token_request['access_token']}"
#
#         return headers
#
#     def get_posts(self, keyword):
#         """
#         Gets the posts of a specified subreddit input: str
#         :return: dict
#         """
#         return get(f"https://oauth.reddit.com/r/{keyword}/new", headers=self.__token,
#                    params={"limit": "1000"}).json()['data']['children']


