from distutils.util import execute
import sqlite3
import os
from datetime import datetime

class PajaroDatabase:

    def __init__(self, config):
        self.config = config
        self.create_db()
        self.create_tables()

    def create_db(self):
        self.db = sqlite3.connect(self.config.get_database_location())
        self.db_cursor = self.db.cursor()

    def create_tables(self):
        try:
            # Posts Table
            self.db_cursor.execute('''
                CREATE TABLE IF NOT EXISTS Posts(
                    Id INTEGER PRIMARY KEY,
                    PostTitle TEXT UNIQUE,
                    PostLink TEXT,
                    PostPublishedDate TEXT,
                    PostHashtags TEXT,
                    Posted TEXT DEFAULT 'FALSE',
                    PostedAt DATETIME DEFAULT NULL,
                    PostID TEXT DEFAULT NULL,
                    LikeCount INTEGER DEFAULT NULL,
                    RetweetCount INTEGER DEFAULT NULL,
                    EntryDate DATETIME DEFAULT (datetime('now','localtime')),
                    UpdatedAt DATETIME DEFAULT (datetime('now','localtime'))
                    )
                ''')
            self.db.commit()

            # Profile Table
            self.db_cursor.execute('''
                CREATE TABLE IF NOT EXISTS Profile(
                    Id INTEGER PRIMARY KEY,
                    FollowerCount INTEGER,
                    FollowingCount INTEGER,
                    PostsCount INTEGER,
                    EntryDate DATETIME DEFAULT (datetime('now','localtime'))
                    )
                ''')
            self.db.commit()

            # Favourited Table
            self.db_cursor.execute('''
                CREATE TABLE IF NOT EXISTS Favourited(
                    Id INTEGER PRIMARY KEY,
                    TweetId TEXT,
                    Caption TEXT,
                    UserName TEXT,
                    CreatedAt TEXT,
                    EntryDate DATETIME DEFAULT (datetime('now','localtime'))
                    )
                ''')
            self.db.commit()

            # Followed Table
            self.db_cursor.execute('''
                CREATE TABLE IF NOT EXISTS Followed(
                    Id INTEGER PRIMARY KEY,
                    UserId TEXT,
                    UserName TEXT,
                    UserLocation TEXT,
                    EntryDate DATETIME DEFAULT (datetime('now','localtime'))
                    )
                ''')
            self.db.commit()

        except Exception as e:
            print("Posts Table Creation Error: {0}", e)

    def insert_into_followed_table(self, tweet):
        try:
            self.db_cursor.execute('''
            INSERT INTO Followed(UserId, UserName, UserLocation)
            VALUES(?,?,?)''', (str(tweet.user.id), str(tweet.screen_name), str(tweet.user.location)))
        except Exception as e:
            print("From Followed table: " + e)
        self.db.commit()

    def insert_into_favourited_table(self, tweet):
        try:
            self.db_cursor.execute('''
            INSERT INTO Favourited(TweetId, Caption, UserName, CreatedAt)
            VALUES(?,?,?,?)''', (str(tweet.id), str(tweet.text), tweet.user.screen_name, tweet.created_at))
        except Exception as e:
            print("From Favourites table: " + e)
        self.db.commit()

    def insert_posts_from_fetcher(self):
        self.db_cursor.execute('''
            SELECT PostTitle, PostLink, PostPublishedDate, PostHashtags from Data
            ORDER BY ID DESC LIMIT ?
        ''', (self.config.get_fetch_limit(),))
        data = self.db_cursor.fetchall()
        data.reverse()
        for post in data:
            try:
                self.db_cursor.execute('''
                    INSERT INTO Posts(PostTitle, PostLink, PostPublishedDate, PostHashtags)
                    VALUES(?,?,?,?)''', (post[0], post[1], post[2], post[3]))
            except Exception:
                pass
        self.db.commit()

    def get_latest_not_posted(self):
        self.db_cursor.execute('''
            SELECT Id, PostTitle, PostLink, PostHashtags from Posts
            WHERE Posted='FALSE' ORDER BY ID DESC LIMIT 1
        ''')
        return self.db_cursor.fetchone()

    def set_post_as_posted(self, id):
        self.db_cursor.execute('''
            UPDATE Posts SET Posted='TRUE' WHERE Id=?
        ''', (id,))
        self.db.commit()

    def update_post_metrics(self, post_id, post):
        self.db_cursor.execute('''
            UPDATE Posts SET PostedAt=?, PostID=?, LikeCount=?, RetweetCount=?, UpdatedAt=(datetime('now','localtime')) WHERE Id=?
        ''', (post.created_at, post.id, post.favorite_count, post.retweet_count, post_id))
        self.db.commit()
