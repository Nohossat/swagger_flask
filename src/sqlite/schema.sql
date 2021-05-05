PRAGMA foreign_keys=ON;

DROP TABLE IF EXISTS tweets;
DROP TABLE IF EXISTS tweets_sentiments;
DROP TABLE IF EXISTS tweets_tags;

CREATE TABLE tweets (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  mediaUrl VARCHAR(300),
  tweetDate VARCHAR(300),
  twitterId VARCHAR(100),
  handle VARCHAR(100),
  text VARCHAR(280) NOT NULL,
  profileUser VARCHAR(100),
  name VARCHAR(50),
  tweetLink VARCHAR(300),
  timestamp VARCHAR(300),
  query VARCHAR(200),
  type VARCHAR(20)
);

CREATE TABLE tweets_sentiments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  tweet_id INTEGER UNIQUE NOT NULL,
  sentiment VARCHAR(10),
  FOREIGN KEY (tweet_id) REFERENCES tweets(id)
);


CREATE TABLE tweets_tags (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  tweet_id INTEGER UNIQUE NOT NULL,
  tags VARCHAR(300),
  FOREIGN KEY (tweet_id) REFERENCES tweets(id)
);
