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

