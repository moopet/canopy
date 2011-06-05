"""
capony - a simple client for the Forrst API

http://forrst.com/api
"""

from urllib import urlencode
from urllib2 import urlopen
from simplejson import load

FORRST_API_ENDPOINT = "api.forrst.com/api/v2"


class ForrstAPIError(Exception):
    pass


class ForrstAPI():
    """The Forrst API allows developers to interact with posts, comments,
    users, and so forth.

    """
    token = None
    use_SSL = True
    is_authenticated = False

    def __init__(self, username=None, password=None, use_SSL=True):
        self.username = username
        self.password = password
        self.use_SSL = use_SSL

    def call_api(self, method, data={}, authenticate=False):
        self.response = None
        if authenticate:
            if self.token:
                data['access_token'] = self.token
            elif self.username and self.password:
                data['email_or_username'] = self.username
                data['password'] = self.password
            else:
                raise ForrstAPIError('authentication required')
        protocol = "https" if self.use_SSL else "http"
        url = "%s://%s/%s" % (protocol, FORRST_API_ENDPOINT, method)
        if data:
            url += "?%s" % urlencode(data)
        response = load(urlopen(url))
        if authenticate and response.get('authed') == 'false':
            raise ForrstAPIError('authentication failure')
        if response.get('stat') == 'ok':
            self.response = response.get('resp', None)
            if authenticate and not self.is_authenticated:
                self.token = self.response.get('token')
                self.is_authenticated = True if self.token else False
            return self.response
        return False

    def stats(self):
        """Return stats about your API usage.
        Note: does not count against your rate limit.

        """
        return self.call_api('stats')

    def users_auth(self):
        """User authentication.
        Provide an email/username and password and get an access token back.

        """
        return self.call_api('users/auth', authenticate=True)

    def users_info(self, username=None, id=None, data={}, authenticate=False):
        """Return user info."""
        if username:
            data['username'] = username
        elif id:
            data['id'] = id
        else:
            raise ForrstAPIError('missing argument: expected username or id')
        return self.call_api('users/info', data=data, authenticate=authenticate)

    def user_posts(self, username=None, id=None, post_type= None, limit=None,
                   after=None, data={}, authenticate=False):
        """Return a user's posts."""
        if username:
            data['username'] = username
        elif id:
            data['id'] = id
        else:
            raise ForrstAPIError('missing argument: expected username or id')
        if post_type:
            data['type'] = post_type
        if limit:
            data['limit'] = limit
        if after:
            data['after'] = after
        if self.call_api('user/posts', data=data, authenticate=authenticate):
            return self.response.get('posts')
        return False

    def posts_show(self, id=None, tiny_id=None, data={}, authenticate=False):
        """Return data about a single post.
        Note: For questions, content is the question.
        For code, content contains the code snippet.
        For code, snaps, and links, description is the post description;
        it is not used for questions.

        """
        if id:
            data['id'] = id
        if tiny_id:
            data['tiny_id'] = tiny_id
        return self.call_api('users/info', data=data, authenticate=authenticate)

    def posts_all(self, after=None, data={}, authenticate=False):
        """Return a list of all posts in reverse-chron order"""
        if after:
            data['after'] = after
        if self.call_api('posts/all', data=data, authenticate=authenticate):
            return self.response.get('posts')
        return False

    def posts_list(self, post_type=None, sort=None, page=None, data={},
                   authenticate=False):
        """Return a list of posts of a given type."""
        if post_type:
            data['post_type'] = post_type
        if sort:
            data['sort'] = sort
        if page:
            data['page'] = page
        if self.call_api('posts/list', data=data, authenticate=authenticate):
            return self.response.get('posts')
        return False

    def post_comments(self, id=None, tiny_id=None, data={}):
        """Return a post's comments."""
        if id:
            data['id'] = id
        if tiny_id:
            data['tiny_id'] = tiny_id
        if self.call_api('post/comments', data=data, authenticate=True):
            return self.response.get('comments')
        return False
