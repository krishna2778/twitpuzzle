from django.db import models

# Create your models here.

class index(models.Model):
    user_id=models.IntegerField()
    user_image_url=models.CharField(max_length=300)
    latest_tweet_id=models.BigIntegerField()
    def __unicode__(self):
        return self.user_image_url


class result(models.Model):
    selected_user_id=models.ForeignKey(index)
    retweeter_user_id=models.IntegerField()
    retweeter_image_url=models.CharField(max_length=300)
    followers_count=models.IntegerField()
    def __unicode__(self):
        return self.retweeter_image_url



class UserDetail(models.Model):
    image_url=models.CharField(max_length=1000)
    twitter_id=models.IntegerField()
    latest_tweet_id=models.BigIntegerField()

class RetweetersUserDetail(models.Model):
    selected_users_id=models.IntegerField()
    retweeters_image_url=models.CharField(max_length=1000)
    retweeters_followers_number=models.IntegerField()