import redis, json
from datetime import datetime
from config import Config

def get_redis():
    pool = redis.ConnectionPool(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=Config.REDIS_DB, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    try:
        r.ping()
    except Exception as e:
        raise RuntimeError(f"Cannot connect to Redis: {e}")
    return r

r = get_redis()

# cache a post (stringified JSON)
def cache_post(post):
    key = f"post:{post['post_id']}"
    for k, v in post.items():
        if isinstance(v, datetime):
            post[k] = v.isoformat()
    r.set(key, json.dumps(post), ex=3600)  # expire in 1 hour
    return True

def get_cached_post(post_id):
    key = f"post:{post_id}"
    data = r.get(key)
    if not data:
        return None
    post = json.loads(data)
    return post

# trending: use sorted set scored by likes
def increment_post_likes_sortedset(post_id, delta=1):
    r.zincrby("trending_posts", delta, post_id)

def get_top_trending(n=10):
    return r.zrevrange("trending_posts", 0, n-1, withscores=True)
