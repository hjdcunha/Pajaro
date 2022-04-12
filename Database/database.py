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
                    CommentCount INTEGER DEFAULT NULL,
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

        except Exception as e:
            print("Posts Table Creation Error: {0}", e)

    def insert_posts_from_fetcher(self):
        self.db_cursor.execute('''
            SELECT PostTitle, PostLink, PostPublishedDate, PostHashtags from Data
            ORDER BY ID DESC LIMIT 10
        ''')
        data = self.db_cursor.fetchall()
        data.reverse()
        for post in data:
            try:
                self.db_cursor.execute('''
                    INSERT INTO Posts(PostTitle, PostLink, PostPublishedDate, PostHashtags)
                    VALUES(?,?,?,?)''', (post[0], post[1], post[2], post[3]))
            except Exception as e:
                print(e)
        self.db.commit()
