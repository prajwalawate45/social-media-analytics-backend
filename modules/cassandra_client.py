import os
os.environ["CASSANDRA_DRIVER_NO_LIBEV"] = "1"
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from cassandra import ConsistencyLevel
from config import Config
import time

cluster = None
session = None

def init_cassandra():
    global cluster, session
    try:
        cluster = Cluster(Config.CASSANDRA_CONTACT_POINTS)
        session = cluster.connect()
        # create keyspace if not exists
        session.execute(f"""
            CREATE KEYSPACE IF NOT EXISTS {Config.CASSANDRA_KEYSPACE}
            WITH REPLICATION = {{ 'class': 'SimpleStrategy', 'replication_factor': '1' }}
        """)
        session.set_keyspace(Config.CASSANDRA_KEYSPACE)
        session.execute("""
            CREATE TABLE IF NOT EXISTS post_events (
                post_id text,
                event_time timestamp,
                event_type text,
                value int,
                PRIMARY KEY (post_id, event_time)
            ) WITH CLUSTERING ORDER BY (event_time DESC)
        """)
    except Exception as e:
        raise RuntimeError(f"Cannot initialize Cassandra: {e}")

# call on import
init_cassandra()

def insert_post_event(post_id, event_type, value=1, event_time=None):
    if event_time is None:
        event_time = int(time.time() * 1000)
    stmt = SimpleStatement(
        "INSERT INTO post_events (post_id, event_time, event_type, value) VALUES (%s, %s, %s, %s)",
        consistency_level=ConsistencyLevel.ONE
    )
    session.execute(stmt, (post_id, event_time, event_type, value))

def get_events_for_post(post_id, limit=50):
    q = SimpleStatement("SELECT post_id, event_time, event_type, value FROM post_events WHERE post_id=%s LIMIT %s")
    rows = session.execute(q, (post_id, limit))
    return list(rows)
