from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from twython import Twython
import operator
from django.template import Context, loader
from djcelery.models import PeriodicTask



def new_get_token():
    APP_KEY = 'b2h7h6oSlYaRQDw5xTbQ'
    APP_SECRET = 's7rhtH9uE6WxWeCWTirvm9rZJIX9ksEGzye0QIII'
    ACCESS_TOKEN='AAAAAAAAAAAAAAAAAAAAAJKdVgAAAAAAjv05kbXIgx%2FvX36F60wlN2%2ByDzw%3DVDHqzjRqXhed6P48hGgqknpB2VWfhmsx5g8P6C22jpN9k63B6V'
    twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
    return twitter


def index(request):
    candidates = {'github':'13334762','twitter':'783214','bill Gates':'50393960','firefox':'2142731','chrome':'56505125','multunus':'98827227','gmail':'38679388','twitterapi':'6253282', 'wordpress':'685513', 'faking':'17381587'}
    imgs = {}
    twitter=new_get_token()
    for candidate_id in candidates.values():
        imageUrl = twitter.show_user(user_id=candidate_id)['profile_image_url_https']
        i=imageUrl.rfind('_')
        imageUrl=imageUrl[:i]+imageUrl[-4:]
        imgs[candidate_id] = imageUrl
    t = loader.get_template('index.html')
    c = Context({'users':imgs})
    return HttpResponse(t.render(c))


def final(uid):
    uid1=uid
    twitter = new_get_token()
    tid = twitter.get_user_timeline(user_id=uid,exclude_replies=True,include_rts=False)[0]['id']
    ls = twitter.get_retweeters_ids(id=tid)
    follow = {}
    retweeters=[]
    imgFormat=['_normal','_mini','_bigger']
    for uid in ls['ids']:
        retweeters.append(twitter.show_user(user_id=uid))
    for user in retweeters:
        url=user['profile_image_url_https']
        for ft in imgFormat:
            if ft in url:
                url="".join(url.split(ft))
                break
        count=user['followers_count']
        follow[url]=count
    rank_list = sorted(follow.items(), key=operator.itemgetter(1))
    rank_list.insert(-10,(twitter.show_user(user_id=uid1)['profile_image_url_https'],'0'))
    return rank_list[-11:]


def result(request, uid):
    twitter=new_get_token()
    r=loader.get_template('result.html')
    sort=final(uid)
    ima=twitter.show_user(user_id=uid)['profile_image_url_https']
    d=Context({'answer':sort,'muthalai':ima})
    return HttpResponse(r.render(d))


