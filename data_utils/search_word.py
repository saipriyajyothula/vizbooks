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
            consumer_key = 'IBcaJgLZNhoRbJL5gk0a22cqS',
            consumer_secret = '58NyTeDQ0tvgwWkHikQLq7lBy0SL13XA5m6MNjxWhme8iJ5Mus',
            access_token = '4896801380-5hVSqPOThxeysVtJw8eyb9pAXS6qcYUih5z4UJc',
            access_token_secret = 'XOX38r1FCqrDIES1QuVNNEedOutRQ7UhyNowLO36te9kp'
         )

        user_names = []
         # this is where the fun actually starts :)
        for tweet in ts.search_tweets_iterable(tso):
            user_names.append(tweet['user']['screen_name'])

        return user_names
    except TwitterSearchException as e: # take care of all those ugly errors if there are some
        print(e) 


def get_randomtext(user):
    """
    Get random text of the user
    """
    try:
        tuo = TwitterUserOrder(user) # create a TwitterUserOrder

        # it's about time to create TwitterSearch object again
        ts = TwitterSearch(
            consumer_key = 'IBcaJgLZNhoRbJL5gk0a22cqS',
            consumer_secret = '58NyTeDQ0tvgwWkHikQLq7lBy0SL13XA5m6MNjxWhme8iJ5Mus',
            access_token = '4896801380-5hVSqPOThxeysVtJw8eyb9pAXS6qcYUih5z4UJc',
            access_token_secret = 'XOX38r1FCqrDIES1QuVNNEedOutRQ7UhyNowLO36te9kp'
        )

        text = []
        # start asking Twitter about the timeline
        for tweet in ts.search_tweets_iterable(tuo):
            text.append(tweet['text'])

        return text
    except TwitterSearchException as e: # catch all those ugly errors
        print(e)



if __name__ == "__main__":
    print get_usernames("emma")
