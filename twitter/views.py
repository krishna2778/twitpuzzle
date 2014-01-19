from django.shortcuts import render

# Create your views here.
from twitter.models import UserDetail
from twitter.models import RetweetersUserDetail
from django.http import HttpResponse
from twython import Twython
import operator
from django.template import Context, loader

candidates = {'github':'13334762','twitter':'783214','bill Gates':'50393960','firefox':'2142731','chrome':'56505125','multunus':'98827227','gmail':'38679388','twitterapi':'6253282', 'wordpress':'685513', 'faking':'17381587'}


def new_get_token():
    APP_KEY = 'b2h7h6oSlYaRQDw5xTbQ'
    APP_SECRET = 's7rhtH9uE6WxWeCWTirvm9rZJIX9ksEGzye0QIII'
    ACCESS_TOKEN='AAAAAAAAAAAAAAAAAAAAAJKdVgAAAAAAjv05kbXIgx%2FvX36F60wlN2%2ByDzw%3DVDHqzjRqXhed6P48hGgqknpB2VWfhmsx5g8P6C22jpN9k63B6V'
    twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
    return twitter


def index(request):
    image_id_users = {}
    global candidates
    twitter_ids = candidates.values()
    for twitter_id in twitter_ids:
         if len(list(UserDetail.objects.filter(twitter_id=twitter_id))) > 1:
             candidate_details = UserDetail.objects.filter(twitter_id=twitter_id).latest("twitter_id")
             print candidate_details
             can_id=candidate_details.twitter_id
             print can_id
             imageUrl = candidate_details.image_url
             i=imageUrl.rfind('_')
             imageUrl=imageUrl[:i]+imageUrl[-4:]
             image_id_users[can_id] = imageUrl
    t = loader.get_template('index.html')
    c = Context({'users':image_id_users})
    print 'In Index'
    return HttpResponse(t.render(c))


def final(uid):
    #retweeters_details=RetweetersUserDetail.objects.filter(selected_users_id=selected_user_id).latest("selected_users_id")
    #retweeters_image=retweeters_details.retweeters_image_url
    #followers_count=retweeters_details.retweeters_followers_number
    #twitter = new_get_token()
    #tid = twitter.get_user_timeline(user_id=uid,exclude_replies=True,include_rts=False)[0]['id']
    #print tid
    #ls = twitter.get_retweeters_ids(id=tid)
    #print ls
    follow = {}
    print 'follow = {}'

    imgFormat=['_normal','_mini','_bigger']
    retweeters_details = []
    selected_user_id=uid
    retweeters_details = list(RetweetersUserDetail.objects.filter(selected_users_id=selected_user_id))
    print retweeters_details
    for details in retweeters_details:
        url = details.retweeters_image_url
        print 'url is '+url
        for delimeter in imgFormat:
            if delimeter in url:
                url = "".join(url.split(delimeter))
                break
        follow[url] = details.retweeters_followers_number

    #for uid in ls['ids']:
    #    retweeters.append(twitter.show_user(user_id=uid))
    #for user in retweeters:
    #    url=user['profile_image_url_https']
    #    for ft in imgFormat:
    #        if ft in url:
    #            url="".join(url.split(ft))
    #            break
    #    count=user['followers_count']
    #    follow[url]=count
    rank_list = sorted(follow.items(), key=operator.itemgetter(1))
    select_user=UserDetail.objects.filter(twitter_id=selected_user_id).latest("twitter_id")
    select_user_image=select_user.image_url
    for delimeter in imgFormat:
        if delimeter in select_user_image:
            select_user_image = "".join(select_user_image.split(delimeter))
            break
    rank_list.insert(-10,(select_user_image,'0'))
    return rank_list[-11:]


def result(request,uid):
   # print 'entered result function'
    sort=final(uid)
    r=loader.get_template('result.html')
    d=Context({'answer':sort})
    return HttpResponse(r.render(d))


