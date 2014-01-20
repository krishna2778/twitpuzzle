from apscheduler.scheduler import Scheduler
from twython import Twython
from twitter.models import UserDetail
from twitter.models import RetweetersUserDetail

started = False
candidates = {'github':'13334762','twitter':'783214','bill Gates':'50393960','firefox':'2142731','chrome':'56505125','multunus':'98827227','gmail':'38679388','twitterapi':'6253282', 'wordpress':'685513', 'faking':'17381587'}
candidates_twitter_id = candidates.values()

def get_new_twitter_object():
    APP_KEY = 'b2h7h6oSlYaRQDw5xTbQ'
    APP_SECRET = 's7rhtH9uE6WxWeCWTirvm9rZJIX9ksEGzye0QIII'
    ACCESS_TOKEN='AAAAAAAAAAAAAAAAAAAAAJKdVgAAAAAAjv05kbXIgx%2FvX36F60wlN2%2ByDzw%3DVDHqzjRqXhed6P48hGgqknpB2VWfhmsx5g8P6C22jpN9k63B6V'
    twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
    return twitter

def get_profile_pic(candidate_id):
    twitter = get_new_twitter_object()
    return twitter.show_user(user_id=candidate_id)['profile_image_url_https']

def get_latest_tweet_id(candidate_id):
    twitter = get_new_twitter_object()
    return twitter.get_user_timeline(user_id=candidate_id,exclude_replies=True,include_rts=False)[0]['id']

def get_retweeters_id(latest_tweet_id):
    twitter = get_new_twitter_object()
    return twitter.get_retweeters_ids(id=latest_tweet_id)

def retweeters_followers(retweeted_user_id):
    twitter = get_new_twitter_object()
    return twitter.show_user(user_id=retweeted_user_id)['followers_count']

def store_detail_to_db(image_url,candidate_id,latest_tweet_id):
    user_detail=UserDetail(image_url=image_url,twitter_id=candidate_id,latest_tweet_id=latest_tweet_id)
    user_detail.save()

def store_retweeters_details_to_db(selected_id1,retweeters_image_url1,retweeters_followers_number1):
    retweeters_details=RetweetersUserDetail(selected_users_id=selected_id1,retweeters_image_url=retweeters_image_url1,retweeters_followers_number=retweeters_followers_number1)
    retweeters_details.save()

sched = Scheduler()

@sched.interval_schedule(minutes=3)
def commit_infinitely():
    global candidates_twitter_id
    if(len(candidates_twitter_id) > 0):
        candidate_id = candidates_twitter_id.pop()
        print "**************** candidate id ****************"
        print candidate_id
        print "**********************************************"
        #getting image url and latest tweet
        image_url = get_profile_pic(candidate_id)
        latest_tweet_id=get_latest_tweet_id(candidate_id)
        store_detail_to_db(image_url,candidate_id,latest_tweet_id)

        #getting retweeters sorted list and followers number
        retweeters_user_id=get_retweeters_id(latest_tweet_id)
        for retweeted_user_id in retweeters_user_id['ids']:
            retweeters_image_url=get_profile_pic(retweeted_user_id)
            retweeters_followers_number=retweeters_followers(retweeted_user_id)
            store_retweeters_details_to_db(candidate_id,retweeters_image_url,retweeters_followers_number)
    else:
        candidates_twitter_id = candidates.values()



if not started:
    sched.start()
    started = True