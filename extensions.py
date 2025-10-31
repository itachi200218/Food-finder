from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
import redis

# Initialize SQLAlchemy
db = SQLAlchemy()

# Initialize MySQL (for direct queries)
mysql = MySQL()

# Redis connection (will be initialized in main.py)
redis_client = None

def init_redis(host):
    global redis_client
    redis_client = redis.StrictRedis(host=host, port=6379, db=0, decode_responses=True)
