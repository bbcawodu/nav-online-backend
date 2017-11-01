from os import environ
import urlparse

# Get Database url from environment variables
urlparse.uses_netloc.append("postgres")
PARSED_DB_URL = urlparse.urlparse(environ["DATABASE_URL"])
