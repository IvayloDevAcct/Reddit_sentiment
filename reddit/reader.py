from requests import auth
from requests import post
from requests import get


"""This module was created before I discovered the praw library. It is not in use, except for the variables"""

# Normally I would get a password and key from secure location
# For this project it's simply coded here
PASSWORD = "RedditTest1234@!"
SECRET_KEY = "35e586IJFTSPq57i5mrNzvQUTIuLfQ"

# Set the API user ID
ID = "4o3BOo3lnIC4dPi5KSA8Jw"


class RedditReader:
    def __init__(self):
        self.__token = self.login()

    def login(self):
        """Authenticates my Reddit user account and creates headers for future API requests
        :returns list"""

        authorization = auth.HTTPBasicAuth(ID, SECRET_KEY)
        # Set request parameters
        data = {
            'grant_type': "password",
            "username": "ivailo_opalchenski",
            "password": PASSWORD
        }
        headers = {'User-Agent': "Version 1"}

        token_request = post("https://www.reddit.com/api/v1/access_token", auth=authorization,
                             data=data, headers=headers).json()

        headers["Authorization"] = f"bearer {token_request['access_token']}"

        return headers

    def get_posts(self, keyword):
        """
        Gets the posts of a specified subreddit input: str
        :return: dict
        """
        return get(f"https://oauth.reddit.com/r/{keyword}/new", headers=self.__token,
                   params={"limit": "1000"}).json()['data']['children']

