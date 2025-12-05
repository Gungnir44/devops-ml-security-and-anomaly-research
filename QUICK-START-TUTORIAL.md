# 30-Minute Hands-On Tutorial: Your DevOps Monitoring Stack

## Mission: Learn by Doing!

### Part 1: Grafana - Build Your First Dashboard (10 min)

**Goal:** Create a live dashboard showing container metrics

1. **Open Grafana:** http://localhost:3000
   - Login: `admin` / `admin`

2. **Verify Data Source:**
   - Left menu → ⚙️ Configuration → Data Sources
   - Should see "Prometheus" already configured
   - If not, click "Add data source" → Prometheus → URL: `http://prometheus:9090`

3. **Create Your First Dashboard:**
   - Click ➕ → Dashboard → Add new panel

4. **Add Container Memory Graph:**
   - In the query box, enter:
     ```
     container_memory_usage_bytes{name=~"devops.*"}
     ```
   - Click "Run query"
   - See live memory usage for all containers!

5. **Customize:**
   - Panel title: "Container Memory Usage"
   - Right side → Panel options → Unit → "bytes(IEC)"
   - Legend: `{{name}}`
   - Click "Apply"

6. **Add CPU Graph:**
   - Click "Add panel" again
   - Query:
     ```
     rate(container_cpu_usage_seconds_total{name=~"devops.*"}[5m])
     ```
   - Title: "Container CPU Usage"
   - Unit: "percent (0.0-1.0)"

7. **Save Dashboard:**
   - Click 💾 Save dashboard
   - Name: "My First DevOps Dashboard"
   - Click "Save"

**Achievement Unlocked:** You just built a professional monitoring dashboard! 🎉

---

### Part 2: PostgreSQL - Database Hands-On (10 min)

**Goal:** Create a database, table, and query data

1. **Open Adminer:** http://localhost:8081

2. **Login to PostgreSQL:**
   - System: `PostgreSQL`
   - Server: `devops-postgres`
   - Username: `demouser`
   - Password: `demopass`
   - Database: `demodb`
   - Click "Login"

3. **Create a Table:**
   - Click "SQL command"
   - Paste this:
     ```sql
     CREATE TABLE users (
       id SERIAL PRIMARY KEY,
       username VARCHAR(50) NOT NULL,
       email VARCHAR(100) NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
     );
     ```
   - Click "Execute"

4. **Insert Data:**
   - SQL command:
     ```sql
     INSERT INTO users (username, email) VALUES
       ('alice', 'alice@example.com'),
       ('bob', 'bob@example.com'),
       ('charlie', 'charlie@example.com');
     ```
   - Execute

5. **Query Data:**
   - SQL command:
     ```sql
     SELECT * FROM users ORDER BY created_at DESC;
     ```
   - Execute

6. **Try Complex Query:**
   ```sql
   SELECT
     username,
     email,
     created_at,
     EXTRACT(EPOCH FROM (NOW() - created_at)) AS seconds_since_creation
   FROM users;
   ```

**Achievement Unlocked:** You just managed a real database! 🗄️

---

### Part 3: RabbitMQ - Message Queues (10 min)

**Goal:** Send and receive messages between services

1. **Open RabbitMQ:** http://localhost:15672
   - Login: `admin` / `adminpass`

2. **Create a Queue:**
   - Top menu → "Queues"
   - Expand "Add a new queue"
   - Name: `order-processing`
   - Click "Add queue"

3. **Send Messages:**
   - Click on your `order-processing` queue
   - Scroll to "Publish message"
   - Payload:
     ```json
     {
       "order_id": 12345,
       "customer": "Alice",
       "items": ["laptop", "mouse"],
       "total": 1299.99
     }
     ```
   - Click "Publish message"

4. **Send More Messages:**
   - Try different payloads:
     ```json
     {"order_id": 12346, "customer": "Bob", "items": ["keyboard"], "total": 89.99}
     ```
     ```json
     {"order_id": 12347, "customer": "Charlie", "items": ["monitor"], "total": 399.99}
     ```

5. **View Messages:**
   - In the queue view, see "Ready" count increase
   - Click "Get messages" → "Get message(s)"
   - See your JSON payloads!

6. **Understand the Flow:**
   - **Producer** (your manual publish) → Queue → **Consumer** (would be an app)
   - Messages wait in queue until consumed
   - This is how microservices communicate asynchronously!

**Achievement Unlocked:** You understand message queues! 📬

---

## Bonus Challenges

### Challenge 1: Prometheus Queries
Open http://localhost:9090 and try:

```promql
# How many containers are up?
count(up{job="cadvisor"})

# Total memory used by all containers
sum(container_memory_usage_bytes{name=~"devops.*"})

# Containers using more than 100MB
container_memory_usage_bytes{name=~"devops.*"} > 100000000
```

### Challenge 2: Multi-Database
1. Connect to MySQL in Adminer (server: `devops-mysql`, user: `appuser`, pass: `apppass`)
2. Create the same `users` table
3. Compare PostgreSQL vs MySQL in Adminer

### Challenge 3: cAdvisor Deep Dive
1. Open http://localhost:8082
2. Find the container using the most CPU
3. Find the container using the most memory
4. Click on a container → see detailed metrics

### Challenge 4: Health Dashboard
1. Open http://localhost:5000
2. Check the API: http://localhost:5000/api/latest
3. Look at the JSON response
4. Understand what health checks are running

---

## Real-World Scenario: Debugging a Problem

**Scenario:** Your app is slow. How do you find the issue?

1. **Grafana:** Check CPU/Memory dashboards
   - Is a container maxed out?

2. **cAdvisor:** Drill into specific container
   - See exact resource usage

3. **Kibana:** Search logs for errors
   - Find exception stack traces

4. **Prometheus:** Query for anomalies
   - Did requests spike?

5. **Database (Adminer):** Check slow queries
   - Is a query taking 10 seconds?

This is **real DevOps troubleshooting!**

---

## What You Learned

✅ **Grafana** - Built a live monitoring dashboard
✅ **PostgreSQL** - Created tables, inserted data, wrote queries
✅ **RabbitMQ** - Sent messages through a queue
✅ **Prometheus** - Queried metrics
✅ **Monitoring Stack** - Understood how it all connects

## Next Level

Want to go deeper? Try:

1. **Set up alerts in Grafana** (email when CPU > 80%)
2. **Write a Python script** that sends messages to RabbitMQ
3. **Configure log shipping** from containers to Elasticsearch
4. **Build a custom exporter** for Prometheus
5. **Create a service** that consumes RabbitMQ messages

---

**Congratulations! You're now hands-on with professional DevOps tools!** 🚀

Return to your curriculum (Module 4: Docker, Module 9: Monitoring) to learn these in-depth.
