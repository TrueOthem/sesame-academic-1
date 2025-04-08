from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.getenv('DB_URL', 'postgresql:///sesame')
SENTRY_DSN = os.environ.get('SENTRY_DSN', None)

# Skip database connection
# import core.db as db
# db.connect(DB_URL)
