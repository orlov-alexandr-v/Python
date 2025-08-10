from authx import AuthXConfig

from dotenv import load_dotenv
from os import getenv

load_dotenv()

config = AuthXConfig(
    JWT_ALGORITHM = "HS256",
    JWT_SECRET_KEY = getenv("SECRET_KEY"),
    JWT_TOKEN_LOCATION = ["cookies"],
    JWT_CSRF_METHODS = [],
    JWT_IMPLICIT_REFRESH_DELTATIME = 3600
    )
