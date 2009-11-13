# NOTE DAVEPECK
#
# I wrote this code to help clients get sessions and users on django + appengine applications.
# It is NOT AT ALL INTERESTING if you don't need users. In fact, for opentransit, I've
# turned if off in the settings.py file. But I kept it here just in case...
# 
# ...this code is based on werkzeug's secure cookie stuff... but heavily modified...
#


import os

from hashlib import sha1
import cPickle as pickle
from hmac import new as hmac
import urllib

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.http import urlquote
from django.template import RequestContext
import django.shortcuts
from django.conf import settings
import simplejson as json

try:
    from functools import update_wrapper
except ImportError:
    from django.utils.functional import update_wrapper  # Python 2.3, 2.4 fallback.


#------------------------------------------------------------------------------
# URL Quoting Helpers
#------------------------------------------------------------------------------

def url_quote(s, charset='utf-8', safe='/:'):
    if isinstance(s, unicode):
        s = s.encode(charset)
    elif not isinstance(s, str):
        s = str(s)
    return urllib.quote(s, safe=safe)

def url_quote_plus(s, charset='utf-8', safe=''):
    if isinstance(s, unicode):
        s = s.encode(charset)
    elif not isinstance(s, str):
        s = str(s)
    return urllib.quote_plus(s, safe=safe)

def url_unquote(s, charset='utf-8', errors='ignore'):
    return urllib.unquote(s).decode(charset, errors)

def url_unquote_plus(s, charset='utf-8', errors='ignore'):
    return urllib.unquote_plus(s).decode(charset, errors)
        

#------------------------------------------------------------------------------
# Django View Helpers
#------------------------------------------------------------------------------

def render_to_response(request, template_name, dictionary={}, **kwargs):
    """
    Similar to django.shortcuts.render_to_response, but uses a RequestContext
    with some site-wide context.
    """
    response = django.shortcuts.render_to_response(
        template_name,
        dictionary,
        context_instance=RequestContext(request),
        **kwargs
    )

    return response

def redirect_to(view, *args, **kwargs):
    """
    Similar to urlresolvers.reverse, but returns an HttpResponseRedirect for the
    URL.
    """
    url = reverse(view, *args, **kwargs)
    response = HttpResponseRedirect(url)
    
    return response
    
def not_implemented(request):
    return render_to_response(request, "not_implemented.html")


#------------------------------------------------------------------------------
# Helpers for login redirection
#------------------------------------------------------------------------------

class _CheckLogin(object):
    """
    Class that checks that the user passes the given test, redirecting to
    the log-in page if necessary. If the test is passed, the view function
    is invoked. The test should be a callable that takes the user object
    and returns True if the user passes.

    We use a class here so that we can define __get__. This way, when a
    _CheckLogin object is used as a method decorator, the view function
    is properly bound to its instance.
    """
    def __init__(self, view_func, test_func, login_url=None, redirect_field_name=settings.REDIRECT_FIELD_NAME):
        if not login_url:
            from django.conf import settings
            login_url = settings.LOGIN_URL
        self.view_func = view_func
        self.test_func = test_func
        self.login_url = login_url
        self.redirect_field_name = redirect_field_name

        # We can't blindly apply update_wrapper because it udpates __dict__ and 
        # if the view function is already a _CheckLogin object then 
        # self.test_func and friends will get stomped. However, we also can't 
        # *not* update the wrapper's dict because then view function attributes
        # don't get updated into the wrapper. So we need to split the
        # difference: don't let update_wrapper update __dict__, but then update
        # the (parts of) __dict__ that we care about ourselves.
        update_wrapper(self, view_func, updated=())
        for k in view_func.__dict__:
            if k not in self.__dict__:
                self.__dict__[k] = view_func.__dict__[k]

    def __get__(self, obj, cls=None):
        view_func = self.view_func.__get__(obj, cls)
        return _CheckLogin(view_func, self.test_func, self.login_url, self.redirect_field_name)

    def __call__(self, request, *args, **kwargs):
        if self.test_func(request.user):
            return self.view_func(request, *args, **kwargs)
        path = urlquote(request.get_full_path())
        tup = self.login_url, self.redirect_field_name, path
        return HttpResponseRedirect('%s?%s=%s' % tup)

def user_passes_test(test_func, login_url=None, redirect_field_name=settings.REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """
    def decorate(view_func):
        return _CheckLogin(view_func, test_func, login_url, redirect_field_name)
    return decorate

def login_required(function=None, redirect_field_name=settings.REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: (u is not None) and (u.is_valid),
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


#------------------------------------------------------------------------------
# Helpers for signed serialization of python objects
#------------------------------------------------------------------------------

class UnquoteError(Exception):
    pass

_timegm = None
def _date_to_unix(arg):
    global _timegm
    if isinstance(arg, datetime):
        arg = arg.utctimetuple()
    elif isinstance(arg, (int, long, float)):
        return int(arg)
    if _timegm is None:
        from calendar import timegm as _timegm
    return _timegm(arg)

def _quote(value):
    return ''.join(pickle.dumps(value).encode('base64').splitlines()).strip()

def _unquote(value):
    try:
        return pickle.loads(value.decode('base64'))
    except:
        raise UnquoteError("whoops.")

def serialize_dictionary(dictionary, secret_key=settings.SERIALIZATION_SECRET_KEY, expires=None):
    secret_key = str(secret_key)    
    if expires:
        dictionary['_expires'] = _date_to_unix(expires)        
    mac = hmac(secret_key, None, sha1)
    result = []
    for key, value in dictionary.iteritems():
        result.append('%s=%s' % (url_quote_plus(key), _quote(value)))
        mac.update('|' + result[-1])        
    return '%s?%s' % (mac.digest().encode('base64').strip(),'&'.join(result))

def deserialize_dictionary(string, secret_key=settings.SERIALIZATION_SECRET_KEY):
    items = None
    if isinstance(string, unicode):
        string = string.encode('utf-8', 'ignore')
    try:
        base64_hash, data = string.split('?', 1)        
    except (ValueError, IndexError):
        items = None
    else:
        items = {}
        mac = hmac(secret_key, None, sha1)
        for item in data.split('&'):
            mac.update('|' + item)
            if not '=' in item:
                items = None
                break
            key, value = item.split('=', 1)
            # try to make the key a string
            key = url_unquote_plus(key)
            try:
                key = str(key)
            except UnicodeError:
                pass
            items[key] = value

        # no parsing error and the mac looks okay, we can now
        # sercurely unpickle our cookie.
        try:
            client_hash = base64_hash.decode('base64')
        except Exception:
            items = client_hash = None
        if items is not None and client_hash == mac.digest():
            try:
                for key, value in items.iteritems():
                    items[key] = _unquote(value)
            except UnquoteError:
                items = None
            else:
                if '_expires' in items:
                    if time() > items['_expires']:
                        items = None
                    else:
                        del items['_expires']
        else:
            items = None
    return items
    
##############
# Misc Helpers
##############

from google.appengine.api.urlfetch import fetch
from datetime import datetime
def get_spreadsheet(key, worksheetId):
    """ gets helpfully formatted data from a google spreadsheet """
    
    jsondata = json.loads( fetch( "http://spreadsheets.google.com/feeds/list/%s/%s/public/values?alt=json"%(key,worksheetId) ).content )

    for entry in jsondata["feed"]["entry"]:
        updated_str = entry['updated']['$t'] 
        updated = datetime.strptime( updated_str[:updated_str.index(".")] , "%Y-%m-%dT%H:%M:%S")
        
        data = dict( [ (k[4:], v['$t']) for k, v in entry.items() if "gsx$" in k ] )
            
        yield {'updated':updated, 'data':data}