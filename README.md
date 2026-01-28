# 🌐 Social Media Analytics Backend using NoSQL Databases

A **Python Flask-based backend system** that demonstrates how multiple **NoSQL databases** — **MongoDB**, **Redis**, **Cassandra**, and **Neo4j**

— can work together to power a scalable, data-driven **Social Media Analytics Platform**.

---

## 📘 Overview

This project simulates a social media backend that supports:

- 👥 Creating users  
- 📝 Adding posts  
- ❤️ Liking posts  
- 📊 Tracking trending content  
- 🔗 Mapping user–post–hashtag relationships  

It showcases **polyglot persistence**, where each database is used for what it does best — combining flexibility, real-time analytics, and graph intelligence.

---

## 🎯 Goals

- 🧩 Build a **unified backend** that integrates multiple NoSQL systems  
- 🧠 Demonstrate **polyglot persistence** with specialized databases  
- ⚡ Implement **real-time analytics** for trends and relationships  
- 🧮 Show scalable, modular backend architecture

---

## 🏗️ Architecture

🔄 Flow Overview
~~~
User / UI
   ↓
Flask REST API (app.py)
   ↓
Data Layer
   ├── MongoDB      → User data
   ├── Redis        → Caching & trending data
   ├── Cassandra    → Time-series post events
   └── Neo4j        → User–post relationships (graph)

~~~

### 💡 Database Roles

| Database       |         Role              |                 Description                                      |
|----------------|---------------------------|------------------------------------------------------------------|
| **MongoDB**    | 🗃️ Flexible Storage      | Stores user profiles and posts as JSON-like documents.            |
| **Redis**      | ⚡ In-Memory Cache       | Maintains cached posts and trending counters with high speed.     |
| **Cassandra**  | 📈 Time-Series Logs      | Efficiently stores and retrieves event logs (likes, posts, etc.). |
| **Neo4j**      | 🔗 Graph Relationships   | Models user, post, and hashtag relationships for analytics.       |

## 📁 Project Structure

```bash
ngd_project/
├── README.md
├── requirements.txt
├── .env.example
├── run_demo.sh
├── app.py
├── config.py
├── report_outline.md
│
├── modules/
│   ├── mongodb_client.py
│   ├── redis_client.py
│   ├── cassandra_client.py
│   └── neo4j_client.py
│
└── scripts/
    ├── init_cassandra.cql
    └── create_neo4j_user_post.cql
---

## ⚙️ Setup Instructions

### 1️⃣ Prerequisites

Ensure the following are installed:

- 🐍 Python **3.10+**
- 🍃 **MongoDB**
- 🔥 **Redis**
- 💎 **Cassandra**
- 🕸️ **Neo4j** Desktop or Server

---

### 2️⃣ Environment Setup

```bash
# Clone the repository
git clone https://github.com/prajwalawate45/social-media-analytics-backend.git
cd social media analytics backend

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Then edit .env with your database credentials and ports
3️⃣ Run Demo Flow
Run the demo script to test full integration:

bash

python app.py --demo
You’ll see output like:


=== Simulate Flow ===
Creating user U1...
Creating post P1...
Liking post P1 twice...
Top Trending: [('P1', 2.0)]
Events for P1: [...]
User posts from graph: [...]
4️⃣ Run Flask API Server
Start the backend server:

bash

python app.py
🔗 Example API Endpoints
Action	    Method           	Endpoint	                    Description
Create       User	      POST    /create_user	          --Create a new user
Create       Post         POST    /create_post	          --Add a post by a user
Like         Post	      POST    /like_post	          --Like an existing post
Top          rending	  GET	/top_trending             --View trending posts
Get         User Posts	  GET	/user_posts/<user_id>     --Retrieve posts from a user

🧪 Example Usage (via curl)
Create a User

bash

curl -X POST -H "Content-Type: application/json" \
-d '{"user_id":"U1","name":"Alice"}' \
http://localhost:5000/create_user
Create a Post

bash

curl -X POST -H "Content-Type: application/json" \
-d '{"post_id":"P1","user_id":"U1","content":"Hello world!", "hashtags":["#intro"]}' \
http://localhost:5000/create_post
View Top Trending Posts

bash

curl http://localhost:5000/top_trending
🧰 Troubleshooting
Issue	Possible Fix
❌ MongoDB not connecting	Ensure mongod service is running
❌ Redis unavailable	Run redis-server or sudo service redis-server start
❌ Cassandra error	Check cqlsh and keyspace initialization
❌ Neo4j auth failure	Verify .env credentials and Neo4j password

🧩 Key Features
Polyglot persistence with 4 NoSQL systems

RESTful API design using Flask

Real-time caching and trending analytics via Redis

Graph-based relationships with Neo4j

Scalable event logging using Cassandra

Modular architecture and clean separation of concerns

🏁 Conclusion
This project demonstrates how multiple NoSQL databases can be integrated into a single intelligent backend for social media analytics.
By combining MongoDB, Redis, Cassandra, and Neo4j, it achieves:

📄 Document flexibility

⚡ Real-time caching

📈 Scalable analytics

🔗 Graph insights

Ideal for modern, data-driven applications that demand speed, scalability, and smart insights.



