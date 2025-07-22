import redis
from dotenv import load_dotenv
import os

load_dotenv()

redis_host=os.getenv('REDIS_HOST')
redis_port=os.getenv('REDIS_PORT')
# Connect to Redis
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0, decode_responses=True)
