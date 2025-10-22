CREATE KEYSPACE IF NOT EXISTS social_media_analytics
WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE social_media_analytics;

CREATE TABLE IF NOT EXISTS post_events (
  post_id text,
  event_time timestamp,
  event_type text,
  value int,
  PRIMARY KEY (post_id, event_time)
) WITH CLUSTERING ORDER BY (event_time DESC);
