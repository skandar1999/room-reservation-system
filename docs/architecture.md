# Room Reservation System Architecture

## Microservices

1.  **user-service** (port 5001):
    -   Purpose: List users.
    -   Endpoint: GET /users (lists all users).
    -   Database: users table (id, email) in the `reservation` database on PostgreSQL.

2.  **salle-service** (port 5002):
    -   Purpose: List rooms and consume Kafka messages (prints messages).
    -   Endpoint: GET /rooms (lists all rooms).
    -   Kafka: Consumes from `reservation-created` topic (prints received messages to the console).
    -   Database: rooms table (id, name) in the `reservation` database on PostgreSQL.

3.  **reservation-service** (port 5003):
    -   Purpose: Create reservations and publish to Kafka.
    -   Endpoint: POST /reservations (creates a reservation, expects JSON payload with `room_id`, `user_id`, `start_time`).
    -   Kafka: Publishes to `reservation-created` topic with details of the created reservation.
    -   Database: reservations table (id, room_id, user_id, start_time) in the `reservation` database on PostgreSQL.

## Technologies

-   Flask: For building the REST APIs for the microservices.
-   PostgreSQL: Stores the application data (users, rooms, reservations) in the `reservation` database.
-   Kafka: Used for asynchronous communication, specifically for the `reservation-created` topic.
-   Docker: Runs the PostgreSQL and Kafka infrastructure.

## Setup

1.  **PostgreSQL:** Run using Docker (command used earlier: `docker run -d --name postgres -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=secret -e POSTGRES_DB=reservation postgres`).
2.  **Kafka:** Requires Zookeeper and Kafka brokers, run using Docker (commands used earlier: `docker run -d --name zookeeper --net my-kafka-network -p 2181:2181 -e ZOOKEEPER_CLIENT_PORT=2181 confluentinc/cp-zookeeper:latest` and `docker run -d --name kafka --net my-kafka-network -p 9092:9092 -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 confluentinc/cp-kafka:latest`).
3.  **Create Kafka Topic:** `docker exec kafka kafka-topics --create --topic reservation-created --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1`.
4.  **Run each service:**
    -   Navigate to each service's directory (`user-service`, `salle-service`, `reservation-service`).
    -   Create and activate a virtual environment: `python3 -m venv venv` and `source venv/bin/activate`.
    -   Install dependencies: `pip install Flask psycopg2-binary confluent-kafka-python`.
    -   Run the application: `python app.py` (or `python3 app.py` if `python` defaults to Python 2).

## Challenges

-   Setting up Kafka with Docker initially involved hostname resolution issues, which were resolved by using a dedicated Docker network (`docker network create my-kafka-network`).
-   Ensuring PostgreSQL connection parameters (database name, user, password, host) were consistent across all services.
-   Remembering to explicitly set the `ZOOKEEPER_CLIENT_PORT` environment variable when running the Zookeeper container.
