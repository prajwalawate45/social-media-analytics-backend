import os
import time
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class Config:
    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "test4545")

def get_driver(retries=5, delay=3):
    """
    Create a Neo4j driver and test the connection.
    Retries a few times in case Neo4j is not ready.
    """
    for attempt in range(1, retries + 1):
        try:
            driver = GraphDatabase.driver(
                Config.NEO4J_URI,
                auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD),
                max_connection_lifetime=1000
            )
            with driver.session() as session:
                session.run("RETURN 1")
            print("✅ Connected to Neo4j successfully!")
            return driver
        except Exception as e:
            if attempt < retries:
                print(f"⚠️ Connection failed (attempt {attempt}/{retries}), retrying in {delay}s...")
                time.sleep(delay)
            else:
                raise RuntimeError(f"❌ Cannot connect to Neo4j after {retries} attempts: {e}")


# Create driver instance
driver = get_driver()

def create_user_node(user_id, name):
    """
    Create or merge a user node with a given user_id and name.
    """
    def _create_user(tx, user_id, name):
        tx.run(
            "MERGE (u:User {user_id:$user_id}) "
            "SET u.name=$name RETURN u",
            user_id=user_id,
            name=name
        )

    with driver.session() as session:
        session.execute_write(_create_user, user_id, name)

def create_post_node_and_relation(post_id, user_id, content, hashtags):
    """
    Create a post node and relate it to the user who posted it.
    """
    def _create_post(tx, post_id, user_id, content, hashtags):
        tx.run(
            """
            MERGE (p:Post {post_id:$post_id})
            SET p.content=$content, p.hashtags=$hashtags
            WITH p
            MATCH (u:User {user_id:$user_id})
            MERGE (u)-[:POSTED]->(p)
            """,
            post_id=post_id,
            content=content,
            hashtags=hashtags,
            user_id=user_id
        )

    with driver.session() as session:
        session.execute_write(_create_post, post_id, user_id, content, hashtags)

def get_user_posts(user_id):
    """
    Retrieve all posts by a specific user (safe session handling).
    """
    def _fetch_user_posts(tx, user_id):
        result = tx.run(
            """
            MATCH (u:User {user_id:$user_id})-[:POSTED]->(p:Post)
            RETURN p.post_id AS post_id, p.content AS content, p.hashtags AS hashtags
            """,
            user_id=user_id
        )
        # Consume result within open transaction
        return [record.data() for record in result]

    with driver.session() as session:
        posts = session.execute_read(_fetch_user_posts, user_id)
        return posts

# Optional: test connection when running this module directly
if __name__ == "__main__":
    driver = get_driver()
