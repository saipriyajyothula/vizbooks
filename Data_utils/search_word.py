from TwitterSearch import *
from get_names import *

def get_usernames(book_name):
    """
    Get user names who have tweeted about the book
    """
    try:
        tso = TwitterSearchOrder() # create a TwitterSearchOrder object
        tso.set_keywords(book_name) # let's define all words we would like to have a look for
        tso.set_include_entities(False) # and don't give us all those entity information

        # it's about time to create a TwitterSearch object with our secret tokens
        ts = TwitterSearch(
            consumer_key = 'aaabbb',
            consumer_secret = 'cccddd',
            access_token = '111222',
            access_token_secret = '333444'
         )

        user_names = []
         # this is where the fun actually starts :)
        for tweet in ts.search_tweets_iterable(tso):
            user_names.append(tweet['user']['screen_name'])

    except TwitterSearchException as e: # take care of all those ugly errors if there are some
        print(e) 

    return user_names

def get_randomtext(user):
    """
    Get random text of the user
    """
    try:
        tuo = TwitterUserOrder(user) # create a TwitterUserOrder

        # it's about time to create TwitterSearch object again
        ts = TwitterSearch(
            consumer_key = 'aaabbb',
            consumer_secret = 'cccddd',
            access_token = '111222',
            access_token_secret = '333444'
        )

        text = []
        # start asking Twitter about the timeline
        for tweet in ts.search_tweets_iterable(tuo):
            text.append(tweet['text'])

    except TwitterSearchException as e: # catch all those ugly errors
        print(e)

    return text

