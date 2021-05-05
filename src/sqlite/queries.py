import sqlite3
import os


def create_connection(action, *args):
    db_file = os.path.join(os.path.dirname(__file__), "tweets.db")
    conn = None
    res = None

    try:
        conn = sqlite3.connect(db_file)
        res = action(conn, *args)
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()
        return res


def create_tables(conn):
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS tweets
                   (id integer primary key autoincrement, mediaUrl, tweetDate, twitterId, handle, text varchar(280), profileUser varchar(100), name varchar(50), tweetLink, timestamp, query, type)''')

    c.execute('''CREATE TABLE IF NOT EXISTS tweets_sentiments
                       (id integer primary key autoincrement, tweet_id, sentiment)''')

    c.execute('''CREATE TABLE IF NOT EXISTS tweets_tags
                           (id integer primary key autoincrement, tweet_id, tags)''')

    # Save (commit) the changes
    conn.commit()

    return "tables created"


def insert_tweets(conn, tweets):
    """

    """
    for tweet in tweets:
        if len(tweet["mediaUrl"]) < 1:
            tweet["mediaUrl"] = ""
        else:
            tweet["mediaUrl"] = ", ".join(tweet["mediaUrl"])

    tweets_values = [tuple(tweet.values()) for tweet in tweets]

    c = conn.cursor()
    c.executemany("insert into tweets (mediaUrl, tweetDate, twitterId, handle, text, profileUser, name, tweetLink, timestamp, query, type) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", tweets_values)
    conn.commit()

    return "done"


def get_tweet_from_id(conn, id):
    c = conn.cursor()
    res = c.execute("select * from tweets where id = '%s';" % id)
    res = res.fetchone()
    conn.commit()

    if res is None:
        raise ValueError("Tweet not found")
    else:
        return res


def get_all_tweet(conn):
    c = conn.cursor()
    res = c.execute("select * from tweets;")
    res = res.fetchall()[0]
    conn.commit()

    if res is None:
        raise ValueError("Tweet not found")
    else:
        return res


def delete_tweet_from_id(conn, id):
    c = conn.cursor()

    # check tweet exists
    is_existing_tweet = c.execute("select * from tweets where id = '%s';" % id)

    if is_existing_tweet.fetchone() is None:
        raise ValueError("Tweet doesn't exist")

    # process deletion
    c.execute("delete from tweets where id = '%s';" % id)

    # confirm deletion
    confirm_deletion = c.execute("select * from tweets where id = '%s';" % id)
    res = confirm_deletion.fetchone()
    conn.commit()

    if res is not None:
        raise ValueError("Tweet not deleted")
    else:
        return "Tweet deleted"


def update_tweet_from_id(id):
    # ici on ajoute le sentiment à un tweet
    for tweet in tweets:
        if len(tweet["mediaUrl"]) < 1:
            tweet["mediaUrl"] = ""
        else:
            tweet["mediaUrl"] = ", ".join(tweet["mediaUrl"])

    tweets_values = [tuple(tweet.values()) for tweet in tweets]

    c = conn.cursor()
    c.executemany("insert into tweets (mediaUrl, tweetDate, twitterId, handle, text, profileUser, name, tweetLink, timestamp, query, type) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", tweets_values)
    conn.commit()

    return "done"



def search_tweet(tags):
    pass


if __name__ == "__main__":
    # create_connection(create_tables)

    tweets = [
        {
            "mediaUrl": [
                "https://pbs.twimg.com/media/Ezk9ybfX0AIb69_.jpg"
            ],
            "tweetDate": "Thu Apr 22 12:24:01 +0000 2021",
            "twitterId": "1976143068",
            "handle": "EmmanuelMacron",
            "text": "Partout en France, le personnel hospitalier s'adapte et innove pour prendre en charge les patients « COVID long ». Leur travail est essentiel, il nous aide à mieux comprendre les différentes formes de la maladie. Grâce à eux, nous la connaissons mieux chaque jour. https://t.co/NmFcLuQeo8",
            "profileUser": "https://twitter.com/EmmanuelMacron",
            "name": "Emmanuel Macron",
            "tweetLink": "https://twitter.com/EmmanuelMacron/status/1385207761886121985",
            "timestamp": "2021-04-26T10:12:58.694Z",
            "query": "https://twitter.com/EmmanuelMacron",
            "type": "tweet"
        }
    ]

    # print(create_connection(insert_tweets, tweets))

    # print(create_connection(get_tweet_from_id, 1))
    print(create_connection(delete_tweet, 3))
    print(create_connection(get_all_tweet))


