# For storing objects/data to disk, here are the native options:
# See also:  https://docs.python.org/3/library/persistence.html
# 1) pickle - works, but no indexing; each call dumps data as another "record"
#             Retrieving data requires reading everything back in - no "random"
#             access possible
# 2) dbm - limited database, only works for strings
# 3) shelve - uses above two to store objects by key, like a dict for file
#             storage; keys used to store data/objects must be unique strings
# 4) sqlite - for a full blown SQL database, deemed overkill in this case
#
import shelve

with shelve.open('tweetdb', protocol=4, writeback=True) as db:
    # db keys must be strings (dbm backend requirement)
    db[key] = obj

