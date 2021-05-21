import sqlite3
import os.path
from utils import timing


class DB(object):

    def __init__(self, outputPath, databName="inverted-index.db", forceRecreate=False):
        dbPath = os.path.join(outputPath, databName)
        if os.path.isfile(dbPath) and forceRecreate:
            print("Forcing an update of the reverse index")
            os.remove(dbPath)
        self.conn = sqlite3.connect(dbPath)
        self.cursor = self.conn.cursor()
        try:
            self.cursor.executescript('''
                CREATE TABLE IF NOT EXISTS IndexWord (
                    word TEXT PRIMARY KEY
                );
                CREATE TABLE IF NOT EXISTS  Posting (
                    word TEXT NOT NULL,
                    documentName TEXT NOT NULL,
                    frequency INTEGER NOT NULL,
                    indexes TEXT NOT NULL,
                    PRIMARY KEY(word, documentName),
                    FOREIGN KEY (word) REFERENCES IndexWord(word)
                );
                CREATE TABLE IF NOT EXISTS Existing(doesExist BOOLEAN NOT NULL CHECK (doesExist IN (0,1)));
            ''')
            self.conn.commit()
        except Exception as err:
            raise Exception(f"Database creation failed: {str(err)}")

    def insertWord(self, wordList):
        try:
            self.cursor.execute("BEGIN TRANSACTION")
            for word in wordList:
                self.cursor.execute("INSERT INTO IndexWord(word) VALUES(?)", [word])
            self.conn.commit()
        except Exception as err:
            raise Exception(f'Inserting into IndexWord table failed : {str(err)}')

    def insertExists(self):
        try:
            self.cursor.execute("INSERT INTO Existing(doesExist) VALUES (?)", [1])
            self.conn.commit()
        except Exception as err:
            raise Exception(f"Inserting into Existing table failed : {str(err)}")

    def getExists(self):
        try:
            self.cursor.execute("SELECT doesExist FROM Existing WHERE doesExist = 1")
            return self.cursor.fetchone() is not None
        except Exception as err:
            raise Exception(f"Query failed {str(err)}")

    def insertPosting(self, postlist):
        try:
            self.conn.execute("BEGIN TRANSACTION")
            for item in postlist:
                self.cursor.execute("INSERT INTO Posting(word, documentName, frequency, indexes) VALUES(?, ?, ?, ?)",
                                    item)
            self.conn.commit()
        except Exception as err:
            raise Exception(f'Inserting into Posting table failed : {str(err)}')

    def getPostingsOfWord(self, listOfWords):
        try:
            query = f"SELECT * FROM Posting WHERE word in ({','.join(['?'] * len(listOfWords))})"
            self.cursor.execute(query, listOfWords)
            rows = self.cursor.fetchall()
            return rows
        except Exception as err:
            raise Exception(f"Failed fetching: {str(err)}")
