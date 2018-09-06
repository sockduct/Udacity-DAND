import configparser
import json
import pandas as pd
import shelve
import sys
import time
# Note:  Depends on current version from GitHub which is newer than v3.6.0 from
#        PyPI!  Must clone repo from GitHUb and install directly per repo
#        instructions.  v3.6.0 api.statuses_lookup method doesn't support
#        tweet_mode parameter.  Also note that when installing the latest
#        version from the GitHub repo, pip/version string will still say it's
#        v3.6.0 even though it's actually newer.  Confirm correct version with
#        >>> import tweepy; help(tweepy.api.statuses_lookup)
#        and confirm that tweet_mode is listed as a parameter.
import tweepy


# Globals:
TWDB = 'twdb'


def get_users(users, twapi, verbose=True):
    '''Retrieve passed user IDs using Twitter API handle.

       Return dict of retrieved IDs, key=ID.
    '''
    userdb = {}

    for i in users:
        user = None
        while True:
            try:
                user = twapi.get_user(i)
            except tweepy.error.RateLimitError as err:
                print(f'Warning:  Caught RateLimitError ({err})')

            if user:
                userdb[user.id_str] = user._json
                break
            else:
                print(f'Warning:  Rate limited at {time.ctime()} - sleeping for a minute '
                       'before retrying...')
                time.sleep(60)

    return userdb


def check_tweets(twids, twapi, verbose=True):
    '''Check on individual tweet IDs.  If ID exists, return details.  If not,
       return error information.

       Return set of found IDs (if any) and dict of tweets key=ID with either
       details or error info.
    '''
    found = set()
    retrieved = {}

    for i in twids:
        tweet = None
        while True:
            save = None
            try:
                tweet = twapi.get_status(i, tweet_mode='extended')
            except tweepy.error.TweepError as err:
                print(f'Warning:  Caught TweepError ({err})')
                save = err
            except tweepy.error.RateLimitError as err:
                print(f'Warning:  Caught RateLimitError ({err})')

            if tweet:
                if verbose:
                    print(f'Info:  Found tweet info for {i}!')
                retrieved[tweet.id_str] = tweet._json
                found.add(i)
                break
            elif save:
                # Save API Status Code and Error Message dict
                retrieved[str(i)] = save.args[0][0]
                break
            else:
                print(f'Warning:  Rate limited at {time.ctime()} - sleeping for a minute '
                       'before retrying...')
                time.sleep(60)

    return found, retrieved


def pace_twgets(twids, twapi):
    '''Pace retrieval of Twitter IDs to deal with rate limiting.'''
    tweets = None
    while True:
        try:
            tweets = twapi.statuses_lookup(twids, include_entities=True,
                                           trim_user=True, tweet_mode='extended')
        except tweepy.error.RateLimitError as err:
            print(f'(Warning:  Caught RateLimitError ({err})')

        if tweets:
            return tweets
        else:
            print(f'Warning:  Rate limited at {time.ctime()} - sleeping for a minute '
                   'before retrying...')
            time.sleep(60)


def get_tweets(twids, twapi, verbose=True):
    '''Retrieve passed tweet IDs using Twitter API handle.
    
       Return set of user IDs, missing tweet IDs and dict of retrieved tweets,
       key=ID.
    '''
    # One at a time:
    # tweet = api.get_status(<id>)
    #
    # Bulk retrieval, up to 100/request:
    # tweets = api.statuses_lookup(<id-list>, include_entities=True)
    twcnt = len(twids)
    # Twitter IDs not able to be successfully retrieved:
    missing = set()
    # Successfully retrieved Twitter IDs:
    retrieved = set()
    # Tweet Data
    tweetdb = {}
    # Twitter User IDs
    users = set()
    
    for i in range(0, len(twids), 100):
        end = i + 100 if i + 100 < twcnt else twcnt
        selids = twids[i:end]
        if verbose:
            print(f'Info:  Attempting retrieval of tweets {i} - {end}...')
        tweets = pace_twgets(selids, twapi)
    
        retrieved.update(tweets.ids())
        # Save tweet IDs that weren't successfully retrieved for later:
        missed = set(selids) - set(tweets.ids())
        if missed:
            if verbose:
                print(f'Warning:  Failed to retrieve tweet(s) {missed}...')
            if any(i in missing for i in missed):
                print(f'Warning:  One or more of tweets not retrieved already in missing!')

            missing.update(missed)
    
        # Save successfully retrieved tweet IDs:
        for tweet in tweets:
            if tweet.id_str in tweetdb:
                print(f'Warning:  Tweet ID {tweet.id_str} already present!')
            uid = tweet.user.id
            if uid not in users:
                if verbose:
                    print('Info:  Found new User ID {uid}.')
                users.add(uid)
            # Using private method
            # Could use alternative parser (see comment in main()) but then
            # loose access to ids method.  Works but fragile...
            tweetdb[tweet.id_str] = tweet._json

    return users, missing, retrieved, tweetdb


def get_twdata(twids):
    '''Retrieve Twitter data and save it in a simple local database.'''
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
    
    # Setup access to Twitter API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)                   
    auth.set_access_token(access_token, access_secret)                          
    # To get back dict instead of native object (tweep.models.<obj>):
    # twapi = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
    # But - loose access to ids method if do this
    twapi = tweepy.API(auth)

    users, missing, retrieved, tweetdb = get_tweets(twids, twapi)
    userdb = get_users(users, twapi)
    found, errordb = check_tweets(missing, twapi)

    if found:
        retrieved.update(found)
        for i in found:
            missing.remove(i)
            tweetdb[str(i)] = secondchk.pop(str(i))

    with shelve.open(TWDB, protocol=4, writeback=True) as db:
        # db keys must be strings (dbm backend requirement)
        db['users'] = users
        db['missing'] = missing
        db['retrieved'] = retrieved
        for tgtdb in [tweetdb, userdb, errordb]:
            for key in tgtdb:
                db[key] = tgtdb[key]


# Passing arguments from sys.argv and parsing them this way is sub-optimal
# It would be better to use argparse or click, but trying to keep this simple
def main(action='update', verbose=True):
    '''Main program entry point.'''
    json_file = None

    if action == 'test':
        # Use test data
        twids = [892420643555336193, 892177421306343426, 891815181378084864,
                 873697596434513921, 842892208864923648]
        action = 'update'
    else:
        # Load Twitter data and extract tweet IDs
        df = pd.read_csv('twitter-archive-enhanced.csv')
        # Convert to native type so usable by tweepy
        twids = list(df.tweet_id)

    if action == 'json-out':
        json_file = 'tweet_json.txt'
        action = 'load'

    if action == 'check':
        if verbose:
            print('Info:  Checking if number of tweet IDs matches number in local '
                  'database...')
        with shelve.open(TWDB, protocol=4) as db:
            missing = db.get('missing')
            retrieved = db.get('retrieved')
        if missing and retrieved and len(missing) + len(retrieved) == len(twids):
            print('Local database up to date.')
            return True
        else:
            print('Local database out of date.')
            return False
    elif action == 'load':
         with shelve.open(TWDB, protocol=4) as db:
            users = db.get('users')
            missing = db.get('missing')
            retrieved = db.get('retrieved')

            if missing and retrieved and users:
                tweetdb = {}
                userdb = {}
                for i in missing:
                    tweetdb[i] = db[str(i)]
                for i in retrieved:
                    tweetdb[i] = db[str(i)]
                for i in users:
                    userdb[i] = db[str(i)]

                if json_file:
                    if verbose:
                        print(f'Info:  Creating file {json_file} with one JSON-encoded'
                               ' tweet per line.')
                    with open(json_file, 'wt') as jfile:
                        for k, v in tweetdb.items():
                            # Add tweet ID for those which couldn't be retrieved
                            if v.get('id') is None:
                                v['id'] = k
                                v['id_str'] = str(k)
                            jfile.write(f'{json.dumps(v)}\n')
                else:
                    return dict(users=users, missing=missing, retrieved=retrieved,
                                tweetdb=tweetdb, userdb=userdb)
            else:
                print('Error:  Database missing/missing information - run update.')
                return
    elif action == 'update':
        if verbose:
            print('Info:  Starting tweet retrieval...')
        get_twdata(twids)
    else:
        sys.exit(f'Error:  Unknown action "{action}".\n'
                  'Usage:  get_tweets [check|update|load|json-out|test]\n'
                  '        --Default action is update--\n')


if __name__ == '__main__':
    main(*sys.argv[1:])

