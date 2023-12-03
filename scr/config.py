from dotenv import load_dotenv
import os

# get environment varrs from .env
load_dotenv()

# get db vars
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

# get another vars
SECRET_AUTH = os.environ.get("SECRET_AUTH")
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
