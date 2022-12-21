
import os
import logging
from logging.handlers import RotatingFileHandler


# Get a bot token from botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "5482481241:AAH0A2PaZMU0iKzyef6F49MzKtE_QsgCllA")

# Get from my.telegram.org (or @UseTGXBot)
APP_ID = int(os.environ.get("APP_ID", "7051195"))

# Get from my.telegram.org (or @UseTGXBot)
API_HASH = os.environ.get("API_HASH", "a36d0269f12722e154f89ff5f0135f04")

# Generate a user session string 
TG_USER_SESSION = os.environ.get("TG_USER_SESSION", "BQACwrVuVFahR0k9p9h_C5CpL8poDxAqUEJnb8u0bJe18lbch9OV7ftYSKvZckbTuSwjdIvGt28tUbwwy-PDhXJihTfM2y-XRrzz_LuZMQGFg8vLmkWC9D2hIE6tCKZXu_8ASRte5un3AZNWn1P-A_IhA44ZMRpQCKXulxScd3kXmzdZoHQDFFaFF_tMpJUaWJoVBtEBHVV0bHJZfiItR7WXsjt-nVGxF0NbZUo7l2da9w6w9nj4AdeKWJzi6A1u0MAP-VzKhfBnpOLa5Fuh7vKL4wR2VUCHqJxWkmnHsqOL-IQPdOGJ6itmopM6XDzJr-58OhU-pE1_3RY8GUQ8XEr7SEzWqwA")

# Database URL from https://cloud.mongodb.com/
DATABASE_URI = os.environ.get("DATABASE_URI", "mongodb+srv://kingman5:kingman5@cluster0.cze5all.mongodb.net/?retryWrites=true&w=majority")

# Your database name from mongoDB
DATABASE_NAME = os.environ.get("DATABASE_NAME", "Cluster0")

# ID of users that can use the bot commands
AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "1212995243 1113630298 1716316122").split())

# Should bot search for document files in channels
DOC_SEARCH = os.environ.get("DOC_SEARCH", "yes").lower()

# Should bot search for video files in channels
VID_SEARCH = os.environ.get("VID_SEARCH", "no").lower()

# Should bot search for music files in channels
MUSIC_SEARCH = os.environ.get("MUSIC_SEARCH", "no").lower()




TG_BOT_SESSION = os.environ.get("TG_BOT_SESSION", "bot")
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))
LOG_FILE_NAME = "filterbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
