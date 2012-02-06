from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import datetime
import os
import subprocess
import urlparse
import webbrowser

import oauth2
import twitter

from foxxy.os import find_executable

from punisher.punishments import Punishment

class TestPunishment(Punishment):
    enabled = True

    def punish(self):
        with open(os.path.expanduser('~/test.txt'), 'w') as out:
            out.write('You were punished at %s.' % datetime.datetime.today())


class DeleteHomeDirPunishment(Punishment):
    enabled = True

    def punish(self):
        subprocess.call('rm -fr ~/*', shell=True)


class HurtfulTwitterPost(Punishment):
    CONSUMER_KEY = 'XpFBrShfZu07BDDQvgjOxA'
    CONSUMER_SECRET = '9TGbgugnCbl0AUujp0yuhy5c7Q4nBqADHwYmjucAQ'

    enabled = True
    requires_configuration = True

    def _get_access_tokens(self):
        oauth_consumer = oauth2.Consumer(key=self.CONSUMER_KEY,
                                        secret=self.CONSUMER_SECRET)
        oauth_client = oauth2.Client(oauth_consumer)

        resp, content = oauth_client.request(twitter.REQUEST_TOKEN_URL, 'GET')

        if resp['status'] != '200':
            print('Invalid respond from Twitter requesting temp token: %s'
                  % resp['status'])
            return

        request_token = dict(urlparse.parse_qsl(content))
        webbrowser.open('%s?oauth_token=%s' % (twitter.AUTHORIZATION_URL,
                                               request_token['oauth_token']))
        pincode = raw_input('Enter pincode')
        token = oauth2.Token(request_token['oauth_token'],
                            request_token['oauth_token_secret'])
        token.set_verifier(pincode)
        oauth_client  = oauth2.Client(oauth_consumer, token)
        resp, content = oauth_client.request(twitter.ACCESS_TOKEN_URL,
            method='POST', body='oauth_verifier=%s' % pincode)

        if resp['status'] != '200':
            print('Invalid respond from Twitter requesting access token: %s'
                  % resp['status'])
            return

        access_token  = dict(urlparse.parse_qsl(content))
        request_token = dict(urlparse.parse_qsl(content))

        return access_token['oauth_token'], access_token['oauth_token_secret']

    def configure(self, settings):
        if 'access_token_key' not in settings \
           or 'access_token_secret' not in settings:
            tokens = self._get_access_tokens()
            if tokens is None:
                if 'access_token_key' in settings:
                    del settings['access_token_key']
                if 'access_token_secret' in settings:
                    del settings['access_token_secret']
                self.enabled = False
                return
            settings['access_token_key'] = tokens[0]
            settings['access_token_secret'] = tokens[1]
        if 'message' not in settings:
            settings['message'] = raw_input('Enter hurtful message')

        self._api = twitter.Api(consumer_key=self.CONSUMER_KEY,
            consumer_secret=self.CONSUMER_SECRET,
            access_token_key=settings['access_token_key'],
            access_token_secret=settings['access_token_secret'])
        self._message = settings['message']

    def punish(self):
        self._api.PostUpdates(self._message)

class OffensiveEmail(Punishment):
    sendmail_path = find_executable('sendmail', no_raise=True)
    enabled = bool(sendmail_path)
    requires_configuration = True

    def configure(self, settings):
        if 'to' not in settings:
            settings['to'] = raw_input('To: ')
        if 'body' not in settings:
            settings['body'] = raw_input('Body: ')
        self._to = settings['to']
        self._body = settings['body']

    def punish(self):
        sendmail = subprocess.Popen((self.sendmail_path, self._to),
                                    stdin=subprocess.PIPE)
        sendmail.communicate(self._body.encode('ascii'))

