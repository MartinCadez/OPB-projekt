import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from flask_caching import Cache

VERSION = "1.0.0"

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_HOST_PORT")

DB_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DB_URI)
cache = Cache(config={"CACHE_TYPE": "SimpleCache"})

DASH_PORT = os.getenv("DASH_PORT")
DASH_HOST = os.getenv("DASH_HOST")
DASH_DEBUG = os.getenv("DASH_DEBUG")
