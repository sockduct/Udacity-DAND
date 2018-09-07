# Tweepy code snippets
import configparser
import tweepy
import sys

# Load secrets
conf = configparser.ConfigParser()
conf.read('secrets.cfg')
consumer_key = conf.get('SECRETS', 'consumer_key', fallback=None)
consumer_secret = conf.get('SECRETS', 'consumer_secret', fallback=None)
access_token = conf.get('SECRETS', 'access_token', fallback=None)
access_secret = conf.get('SECRETS', 'access_secret', fallback=None)
if not all([consumer_key, consumer_secret, access_token, access_secret]):
    sys.exit('Error:  Expecting populated "secrets.cfg" file.  See secrets.exmpl for'
             ' expected layout.')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)                   
auth.set_access_token(access_token, access_secret)                          
                                                                            
api = tweepy.API(auth)                                                      
# Or - to get back dict instead of native object (tweep.models.<obj>):
# api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# One at a time:
tweet = api.get_status(892420643555336193)

# Bulk retrieval, up to 100/request:
tweets = api.statuses_lookup(<id-list>, include_entities=True)

# If get native object use this to get dict:
tweet._json


# Handle rate limiting:
# In this example, the handler is time.sleep(15 * 60),
# but you can of course handle it in any way you want.
def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)

for follower in limit_handled(tweepy.Cursor(api.followers).items()):
    if follower.friends_count < 300:
        print(follower.screen_name)


# Iterating through items/pages of data with Cursor:
# # is optional, default is all
for status in tweepy.Cursor(api.user_timeline).items(#):
    # process status here
    process_status(status)

# Iterating through pages:
# # is optional, default is all
for page in tweepy.Cursor(api.user_timeline).pages(#):
    # page is a list of statuses
    process_page(page)


# Pass parameters into API method:
api.user_timeline(id="twitter")


# Pass parameters to Cursor via constructor:
tweepy.Cursor(api.user_timeline, id="twitter")

