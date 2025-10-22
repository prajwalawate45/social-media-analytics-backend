from pymongo import MongoClient, errors
from datetime import datetime
from config import Config

def get_mongo_client():
    try:
        client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        return client
    except errors.PyMongoError as e:
        raise RuntimeError(f"Cannot connect to MongoDB: {e}")

client = get_mongo_client()
db = client[Config.MONGO_DB]
users_coll = db['users']
posts_coll = db['posts']

# helpful functions
def create_user(user_id, name):
    user = {"user_id": user_id, "name": name, "joined_at": datetime.utcnow()}
    users_coll.update_one({"user_id": user_id}, {"$setOnInsert": user}, upsert=True)
    return user

def create_post(post_id, user_id, content, hashtags=None):
    if hashtags is None:
        hashtags = []
    post = {
        "post_id": post_id,
        "user_id": user_id,
        "content": content,
        "hashtags": hashtags,
        "created_at": datetime.utcnow(),
        "likes": 0
    }
    posts_coll.update_one({"post_id": post_id}, {"$setOnInsert": post}, upsert=True)
    return post

def get_posts_for_user(user_id):
    return list(posts_coll.find({"user_id": user_id}, {"_id": 0}))
