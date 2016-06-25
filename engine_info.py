#Engine Info
import tweepy

o_kinect = 'PSNPSUPT/suptpsnp@10.54.142.155:1521/P169i0'

pd_kinect = 'mysql+pymysql://pharm27:Ami7into@data.mdlzsupply.com/pharmdata'

email_login = {
				'user':'pharmbotpi@gmail.com',
				'pw':'Ami7into',
				'receiver':'phillip.harm@mdlz.com'
				}



class TwitterAPI:
    def __init__(self):
        consumer_key = "sjpy37rGXE3HCgVfJEx3eMy28"
        consumer_secret = "g9niWDOtY4KqAxdfoxKkHX7WMx2u1WUZwRjsimdPOxiErPh773"
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        access_token = "4063957228-vgLcuwFuW8RMVhr87ukRN6sPE6m7M1vKYtJyzyd"
        access_token_secret = "y6ky1kUnKbJUdBAcSKlXQpKMkBSbxoJHyDvYrtwmQwhrz"
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def tweet(self, message):
        self.api.update_status(status=message)
        