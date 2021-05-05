import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
from src.util import compute_sentiment

# CREATE DB OBJECT
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys=ON;")

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('sqlite/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


# CRUD OPERATIONS
def insert_tweets(tweets):
    db = get_db()

    final_results = []

    for tweet in tweets:
        if len(tweet["mediaUrl"]) < 1:
            tweet["mediaUrl"] = ""
        else:
            tweet["mediaUrl"] = ", ".join(tweet["mediaUrl"])

        res = db.execute("insert into tweets (mediaUrl, tweetDate, twitterId, handle, text, profileUser, name, tweetLink, timestamp, query, type) values (:mediaUrl, :tweetDate, :twitterId, :handle, :text, :profileUser, :name, :tweetLink, :timestamp, :query, :type)", tweet)

        if res is None:
            raise ValueError(f"Can't insert tweet this tweet: {tweet['twitterId']}")
        else:
            db.execute("insert into tweets_sentiments (tweet_id, sentiment) values (?, ?)",
                       (res.lastrowid, tweet["sentiment"]))
            final_tweet = db.execute("SELECT *, tweets_sentiments.sentiment FROM tweets LEFT JOIN tweets_sentiments ON tweets_sentiments.tweet_id = tweets.rowid WHERE tweets.rowid = '%s';" % res.lastrowid).fetchone()
            final_results.append(dict(final_tweet))
            print(res.lastrowid, flush=True)

    db.commit()
    return final_results


def get_tweet_from_id(id):
    db = get_db()

    res = db.execute("SELECT *, tweets_sentiments.sentiment FROM tweets LEFT JOIN tweets_sentiments ON tweets_sentiments.tweet_id = tweets.rowid WHERE tweets.rowid = '%s';" % id).fetchone()

    if res is None:
        raise ValueError("Tweet not found")
    else:
        return dict(res)


def get_all_tweet(conn):
    c = conn.cursor()
    res = c.execute("select * from tweets;")
    res = res.fetchall()
    conn.commit()

    if res is None:
        raise ValueError("Tweet not found")
    else:
        return res


def delete_tweet_from_id(id):
    db = get_db()

    # check tweet exists
    is_existing_tweet = db.execute("select * from tweets where rowid = '%s';" % id)

    if is_existing_tweet.fetchone() is None:
        raise ValueError("Tweet doesn't exist")

    # process deletion
    db.execute("delete from tweets where id = '%s';" % id)

    # confirm deletion
    confirm_deletion = db.execute("select * from tweets where rowid = '%s';" % id)
    res = confirm_deletion.fetchone()
    db.commit()

    if res is not None:
        raise ValueError("Tweet not deleted")
    else:
        return "Tweet deleted"


def get_sentiment_to_tweet_from_id(id):
    db = get_db()

    # get tweet
    tweet = get_tweet_from_id(id)

    prediction = compute_sentiment([tweet["text"]])

    try:
        db.execute(f"UPDATE tweets_sentiments SET sentiment = '%s' WHERE tweet_id = '%s'" % (prediction, id))
        res = db.execute("SELECT *, tweets_sentiments.sentiment FROM tweets LEFT JOIN tweets_sentiments ON tweets_sentiments.tweet_id = tweets.rowid WHERE tweets.rowid = '%s';" % id).fetchone()
        db.commit()

        if res is None:
            raise ValueError("Tweet not found")
        else:
            print(dict(res), flush=True)
            return dict(res)
    except sqlite3.IntegrityError:
        raise ValueError("This tweet doesn't exist")


def search_tweet(tags):
    pass


if __name__ == "__main__":

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
        },
        {
            "mediaUrl": [
                "https://pbs.twimg.com/media/EynpuoTWEAoo4zs.jpg"
            ],
            "tweetDate": "Sat Apr 10 14:33:45 +0000 2021",
            "twitterId": "1976143068",
            "handle": "EmmanuelMacron",
            "text": "À vous, agriculteurs qui, partout en France, avez lutté sans relâche, nuit après nuit, pour protéger les fruits de votre travail, je veux vous dire notre soutien plein et entier dans ce combat. Tenez bon ! Nous sommes à vos côtés et le resterons. https://t.co/uaW9TmPxYh",
            "profileUser": "https://twitter.com/EmmanuelMacron",
            "name": "Emmanuel Macron",
            "tweetLink": "https://twitter.com/EmmanuelMacron/status/1380891759652265986",
            "timestamp": "2021-04-26T10:12:58.695Z",
            "query": "https://twitter.com/EmmanuelMacron",
            "type": "tweet"
        }

    ]

    print(get_sentiment_to_tweet_from_id(1))

