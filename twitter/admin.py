from twitter.models import index
from twitter.models import result
from django.contrib import admin


class details(admin.ModelAdmin):
    fieldsets = [
        ('User ID',{'fields':['user_id']}),
        ('User Image URL',{'fields':['user_image_url']}),
        ('Latest Tweet ID',{'fields':['latest_tweet_id']})


    ]

admin.site.register(index, details)

class detailsresult(admin.ModelAdmin):
    fieldsets = [
        ('Selected users ID', {'fields':['selected_user_id']}),
        ('Retweeter User ID',{'fields':['retweeter_user_id']}),
        ('Retweeter Image URL',{'fields':['retweeter_image_url']}),
        ('Followers Count',{'fields':['followers_count']})



    ]
admin.site.register(result,detailsresult)