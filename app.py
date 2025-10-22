from flask import Flask, jsonify, request
from config import Config
from modules.mongodb_client import create_user, create_post, get_posts_for_user
from modules.redis_client import cache_post, get_cached_post, increment_post_likes_sortedset, get_top_trending
from modules.cassandra_client import insert_post_event, get_events_for_post
from modules.neo4j_client import create_user_node, create_post_node_and_relation, get_user_posts

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({"status":"ok"}), 200

@app.route('/create_user', methods=['POST'])
def api_create_user():
    data = request.json
    uid = data.get('user_id')
    name = data.get('name')
    if not uid or not name:
        return jsonify({"error":"user_id and name required"}), 400

    user = create_user(uid, name)
    # also put into graph
    create_user_node(uid, name)
    return jsonify({"user": user}), 201

@app.route('/create_post', methods=['POST'])
def api_create_post():
    data = request.json
    pid = data.get('post_id')
    uid = data.get('user_id')
    content = data.get('content')
    hashtags = data.get('hashtags', [])
    if not pid or not uid or not content:
        return jsonify({"error":"post_id, user_id and content required"}), 400

    post = create_post(pid, uid, content, hashtags)
    cache_post(post)
    insert_post_event(pid, 'create', 1)
    # trending seed
    increment_post_likes_sortedset(pid, 0)
    # neo4j
    create_post_node_and_relation(pid, uid, content, hashtags)
    return jsonify({"post": post}), 201

@app.route('/like_post', methods=['POST'])
def api_like_post():
    data = request.json
    pid = data.get('post_id')
    if not pid:
        return jsonify({"error":"post_id required"}), 400
    # increment trending sorted set
    increment_post_likes_sortedset(pid, 1)
    insert_post_event(pid, 'like', 1)
    return jsonify({"status":"liked", "post_id": pid}), 200

@app.route('/post/<post_id>')
def get_post(post_id):
    # check cache first
    cached = get_cached_post(post_id)
    events = get_events_for_post(post_id)
    return jsonify({"cached": cached, "events_count": len(events)})

@app.route('/top_trending')
def top_trending():
    items = get_top_trending(10)
    return jsonify({"trending": items})

@app.route('/user_posts/<user_id>')
def user_posts(user_id):
    posts = get_posts_for_user(user_id)
    graph_posts = get_user_posts(user_id)
    return jsonify({"mongo_posts": posts, "graph_posts": graph_posts})

def simulate_flow():
    print("=== Simulate Flow ===")
    # create user
    print("Creating user U1...")
    create_user("U1", "Alice")
    create_user_node("U1", "Alice")
    # create post
    print("Creating post P1...")
    create_post("P1", "U1", "Hello world from NGD project #intro", ["#intro"])
    cache_post({"post_id":"P1", "user_id":"U1", "content":"Hello world from NGD project #intro"})
    create_post_node_and_relation("P1", "U1", "Hello world from NGD project #intro", ["#intro"])
    insert_post_event("P1", "create", 1)
    # like post
    print("Liking post P1 twice...")
    for _ in range(2):
        increment_post_likes_sortedset("P1", 1)
        insert_post_event("P1", "like", 1)
    print("Top Trending:", get_top_trending(5))
    print("Events for P1:", get_events_for_post("P1"))
    print("User posts from graph:", get_user_posts("U1"))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--demo', action='store_true', help='run simulate_flow then exit')
    args = parser.parse_args()
    if args.demo:
        simulate_flow()
    else:
        app.run(host=Config.FLASK_HOST, port=Config.FLASK_PORT, debug=True)
