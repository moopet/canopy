"""
fapfapfAPI
"""

from urllib import urlencode
from urllib2 import urlopen
from simplejson import loads

FORRST_API_ENDPOINT = "api.forrst.com/api/v2"


class ForrstAPIError(Exception):
    pass


class ForrstAPI():
    token = None

    def __init__(self, username=None, password=None, use_SSL=True):
        self.username = username
        self.password = password
        self.endpoint = "https://" if use_SSL else "http://"
        self.endpoint += FORRST_API_ENDPOINT

    def call_api(self, method, data={}, authenticate=False):
        if authenticate:
            if self.token:
                data['token'] = self.token
            elif self.username and self.password:
                data['username'] = self.username
                data['password'] = self.password
            else:
                raise ForrstAPIError('authentication required')
        url = "%s/%s" % (self.endpoint, method)
        if data:
            url += "?%s" % urlencode(data)
        json_response = urlopen(url).read()
        response = loads(json_response)
        if response.get('stat', '') == 'ok':
            self.response = response.get('resp', None)
            return self.response
        else:
            self.response = None
            return False

    def users_auth(self):
        return self.call_api('users/auth', authenticate=True)

    def stats(self):
        return self.call_api('stats')

    def users_info(self, data={}, authenticate=False):
        return self.call_api('users/info', data=data, authenticate=authenticate)

    def user_posts(self, data={}, authenticate=False):
        return self.call_api('user/posts', data=data, authenticate=authenticate)

    def posts_show(self, data={}, authenticate=False):
        return self.call_api('users/info', data=data, authenticate=authenticate)

    def posts_list(self, data={}, authenticate=False):
        return self.call_api('posts/list', data=data, authenticate=authenticate)

    def post_comments(self, data={}, authenticate=False):
        return self.call_api('post/comments', data=data, authenticate=authenticate)
