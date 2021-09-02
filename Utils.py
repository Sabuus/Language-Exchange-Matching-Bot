import os
from dotenv import load_dotenv

load_dotenv()

DB = os.getenv("DB")
USER = os.getenv("USER")
PASS = os.getenv("PASS")
HOST = os.getenv("HOST")
SCHEMA = os.getenv("SCHEMA")
TOKEN = os.getenv("DISCORD_TOKEN")