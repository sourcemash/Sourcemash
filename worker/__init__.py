import os


def create_worker(env=None):

  import redis

  redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

  conn = redis.from_url(redis_url)

  return conn
