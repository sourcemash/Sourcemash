import os
import redis

def create_worker(env=None):
  redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
  conn = redis.from_url(redis_url)

  return conn
