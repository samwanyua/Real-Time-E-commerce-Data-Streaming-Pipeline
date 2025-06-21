## Real-Time E-commerce Data Streaming Pipeline

This project demonstrates a real-time data engineering pipeline for an e-commerce platform using some of the industry's most powerful technologies:

- **Apache Kafka + Zookeeper** for real-time event streaming
- **Apache Flink** for stream processing and aggregation
- **PostgreSQL** for storing raw and enriched transactional data
- **Elasticsearch** for fast, flexible search and analytics
- **Kibana** for visualizing real-time insights
- **Docker Compose** to containerize the entire stack

---

## Use Case

Simulated user behavior on an e-commerce site, such as:

- Viewing products
- Adding items to a cart
- Completing purchases

These actions generate events, which are streamed through Kafka, processed by Flink, stored in PostgreSQL, indexed in Elasticsearch, and visualized in Kibana.

---

##  Architecture

```text
+-------------+        +--------+       +--------+       +-------------+
|  Event Gen  +------> | Kafka  +-----> | Flink  +-----> | PostgreSQL  |
|  (Producer) |        +--------+       +--------+       +-------------+
       |                                     |
       |                                     v
       |                              +--------------+
       |                              | Elasticsearch |
       |                              +--------------+
       |                                     |
       v                                     v
+--------------+                      +--------------+
| Zookeeper    |                      |   Kibana     |
+--------------+                      +--------------+
```

## 🛠 Tech Stack

| Layer         | Technology        | Purpose                           |
|---------------|-------------------|-----------------------------------|
| Ingestion     | Apache Kafka      | Stream event ingestion            |
| Coordination  | Apache Zookeeper  | Manage Kafka cluster metadata     |
| Processing    | Apache Flink      | Real-time transformation & ETL    |
| Storage       | PostgreSQL        | Store raw/enriched data           |
| Analytics     | Elasticsearch     | Indexing & search                 |
| Dashboarding  | Kibana            | Visual insights                   |
| Orchestration | Docker Compose    | Containerized local environment   |


## Getting Started
1. Clone the Repository
```
git clone https://github.com/samwanyua/Real-Time E-commerce Data Streaming Pipeline.git
cd Real-Time E-commerce Data Streaming Pipeline
```

2. Start All Services
```
docker-compose up -d
```
This will spin up: Kafka + Zookeeper, Flink (JobManager & TaskManager), PostgreSQL, Elasticsearch,Kibana

3. Generate Events
Simulate e-commerce events with the Python Kafka producer:

```
python kafka-producer/producer.py
```
Each event looks like:

```
{
  "event_type": "purchase",
  "user_id": "user_123",
  "product_id": "product_456",
  "amount": 299.99,
  "timestamp": 1720798021
}
```

4. Deploy the Flink Job
Run the Flink processing job that:

Aggregates purchase amounts per product

Sends results to Elasticsearch and PostgreSQL

```
docker exec -it flink-jobmanager ./bin/pyflink.sh flink-job/process_orders.py
```
5. Explore the Data
```
docker exec -it postgres psql -U ecommerce -d ecommerce
```
🔍 Elasticsearch
Query processed results:

```
curl -X GET "localhost:9200/sales-agg/_search?pretty"
```
📊 Kibana
Access Kibana at http://localhost:5601

