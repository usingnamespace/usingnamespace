import base64
import binascii
import datetime
import hashlib
import hmac
import json

from pyramid.compat import (
    long,
    text_type,
    binary_type,
    url_unquote,
    url_quote,
    bytes_,
    ascii_native_,
    )

from pyramid.util import strings_differ

class CookieHelper(object):
    """
    A helper class that helps bring some sanity to the insanity that is cookie
    handling.

    By default this will create a single cookie, given a value it will base64
    encode it, then using HMAC cryptograpphically sign the data. This way a
    remote user can not tamper with it.
    """

    serialize = lambda self, v: json.dumps(v)
    deserialize = lambda self, v: json.loads(v)

    def __init__(self,
            secret,
            salt,
            cookie_name,
            secure=False,
            max_age=None,
            http_only=False,
            path="/",
            wild_domain=False,
            parent_domain=False,
            domain=None,
            hashalg='sha512',
            ):

        self.secret = secret
        self.salt = salt
        self.cookie_name = cookie_name
        self.secure = secure
        self.max_age = max_age
        self.http_only = http_only
        self.path = path
        self.wild_domain = wild_domain
        self.parent_domain = parent_domain
        self.domain = domain
        self.hashalg = hashalg

        self.digestmod = lambda: hashlib.new(self.hashalg)
        self.digest_size = self.digestmod().digest_size

        self.salted_secret = bytes_(salt or '') + bytes_(secret)

        static_flags = []
        if self.secure:
            static_flags.append('; Secure')
        if self.http_only:
            static_flags.append('; HttpOnly')
        self.static_flags = "".join(static_flags)

    def signed_serialize(self, appstruct):
        """Given an appstruct it serializes and signs the data
        """

        cstruct = self.serialize(appstruct)
        sig = hmac.new(self.salted_secret, cstruct, self.digestmod).digest()
        return base64.b64encode(cstruct + sig)

    def signed_deserialize(self, bstruct):
        """Given an bstruct is verifies the signature and then deserializes the
        data
        """

        try:
            fstruct = base64.b64decode(bstruct)
        except (binascii.Error, TypeError) as e:
            raise ValueError('Badly formed base64 data: %s' % e)

        cstruct = fstruct[:-self.digest_size]
        expected_sig = fstruct[-self.digest_size:]

        sig = hmac.new(self.salted_secret, cstruct, self.digestmod).digest()
        if strings_differ(sig, expected_sig):
            raise ValueError('Invalid signature')

        return self.deserialize(cstruct)

    def raw_headers(self, request, value, max_age=None):
        """ Retrieve raw headers for setting cookies

        This returns a list of headers that should be set for the cookies to be
        correctly set.
        """

        bstruct = self.signed_serialize(value)

        return self._get_cookies(request.environ, bstruct, max_age=max_age)

    def set_cookie(self, request, value, max_age=None, response=None):
        """ Set the cookie on a response

        If response is not passed in, it will get it from the current request
        """
        if response is None:
            response = request.response

        cookies = self.raw_headers(request, value, max_age=max_age)

        response.headerlist.append(cookies)

        return response

    def get_cookie(self, request):
        """ Looks for a cookie by name, and returns its value

        Looks for the cookie in the cookies jar, and if it can find it it will
        attempt to deserialize it. Throws a ValueError if it fails due to an
        error, or returns None if there is no cookie.
        """
        cookie = request.cookies.get(self.cookie_name)

        if cookie is None:
            return None

        return self.signed_deserialize(cookie)

    def _get_cookies(self, environ, value, max_age=None):
        """Internal function

        This returns a list of cookies that are valid HTTP Headers.

        :environ: The request environment
        :value: The value to store in the cookie
        """

        # Length selected based upon http://browsercookielimits.x64.me
        if len(value) > 4093:
            raise ValueError(
                'Cookie value is too long to store (%s bytes)' %
                len(value)
                )

        if max_age is None:
            max_age = ''
        elif max_age <= 0:
            max_age = "; Max-Age=0; Expires=Wed, 31-Dec-97 23:59:59 GMT"
            value = ''
        else:
            later = datetime.datetime.utcnow() + datetime.timedelta(
                seconds=int(max_age))
            # Wdy, DD-Mon-YY HH:MM:SS GMT
            expires = later.strftime('%a, %d %b %Y %H:%M:%S GMT')
            # the Expires header is *required* at least for IE7 (IE7 does
            # not respect Max-Age)
            max_age = "; Max-Age=%s; Expires=%s" % (max_age, expires)

        cur_domain = environ.get('HTTP_HOST', environ.get('SERVER_NAME'))

        # While Chrome, IE, and Firefox can cope, Opera (at least) cannot
        # cope with a port number in the cookie domain when the URL it
        # receives the cookie from does not also have that port number in it
        # (e.g via a proxy).  In the meantime, HTTP_HOST is sent with port
        # number, and neither Firefox nor Chrome do anything with the
        # information when it's provided in a cookie domain except strip it
        # out.  So we strip out any port number from the cookie domain
        # aggressively to avoid problems.  See also
        # https://github.com/Pylons/pyramid/issues/131
        if ':' in cur_domain:
            cur_domain = cur_domain.split(':', 1)[0]

        domains = []
        if self.domain:
            domains.append(self.domain)
        else:
            if self.parent_domain and cur_domain.count('.') > 1:
                domains.append('.' + cur_domain.split('.', 1)[1])
            else:
                domains.append(None)
                domains.append(cur_domain)
                if self.wild_domain:
                    domains.append('.' + cur_domain)

        cookies = []
        base_cookie = '%s="%s"; Path=%s%s%s' % (self.cookie_name, value,
                self.path, max_age, self.static_flags)
        for domain in domains:
            domain = '; Domain=%s' % domain if domain is not None else ''
            cookies.append(('Set-Cookie', '%s%s' % (base_cookie, domain)))

        return cookies

