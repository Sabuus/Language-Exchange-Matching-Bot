import os
from dotenv import load_dotenv

load_dotenv()

DB = os.getenv("DB")
USER = os.getenv("USER")
PASS = os.getenv("PASS")
HOST = os.getenv("HOST")
TOKEN = os.getenv("DISCORD_TOKEN")