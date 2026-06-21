import os

class Config:
    CLIENT_ID = os.environ.get("CLIENT_ID")
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
    CLIENT_TOKEN = os.environ.get("CLIENT_TOKEN")
    DATABASE = 'polls.db'
    AUTH_MODE = 'auth'


