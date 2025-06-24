## Real-Time E-commerce Data Streaming Pipeline (Kafka + Spark + ELK + PostgreSQL)

This project demonstrates a **real-time streaming data pipeline** for an e-commerce platform using:

- **Apache Kafka** for event ingestion  
- **Apache Spark Structured Streaming** for real-time processing  
- **PostgreSQL** for storing transactional data  
- **Elasticsearch** for search & analytics  
- **Kibana** for real-time dashboards  
- **Docker Compose** to run the entire stack locally

---

##  Use Case

Simulated user activity from an e-commerce app, including:

- Product views  
- Cart additions  
- Purchase events  

These actions generate events streamed through Kafka, processed by Spark, stored in PostgreSQL, indexed in Elasticsearch, and visualized using Kibana.

---

##  Architecture

```text
+-------------+        +--------+        +--------+        +-------------+
|  Producer   +------> | Kafka  +------> | Spark  +------> | PostgreSQL  |
| (Python App)|        +--------+        +--------+        +-------------+
       |                                      |
       |                                      v
       |                               +--------------+
       |                               | Elasticsearch |
       |                               +--------------+
       |                                      |
       v                                      v
+--------------+                       +--------------+
|  Zookeeper   |                       |    Kibana    |
+--------------+                       +--------------+
```

##  Stack Breakdown +  Getting Started

###  Stack Breakdown

| Layer         | Tool                   | Description                            |
|---------------|------------------------|----------------------------------------|
| Ingestion     | **Kafka**              | Real-time event streaming              |
| Coordination  | **Zookeeper**          | Kafka broker metadata manager          |
| Processing    | **Spark Structured Streaming** | Real-time transformation & aggregation |
| Storage       | **PostgreSQL**         | Stores raw and processed data          |
| Indexing      | **Elasticsearch**      | Fast search and analytics              |
| Dashboarding  | **Kibana**             | Data exploration & visualization       |
| Orchestration | **Docker Compose**     | Local container orchestration          |

---

###  Getting Started

#### 1. Clone the Repository

```bash
git clone https://github.com/samwanyua/real-time-ecommerce-streaming-pipeline.git
cd real-time-ecommerce-streaming-pipeline
```

2. Start All Services
```
docker-compose up -d
```
This will spin up: Kafka + Zookeeper, PostgreSQL, Elasticsearch,Kibana

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

4.  Run the Spark Streaming Job
```
docker exec -it spark-master /spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \
  /app/spark_job.py```

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

