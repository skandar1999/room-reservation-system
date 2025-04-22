from flask import Flask, jsonify
import psycopg2
from confluent_kafka import Consumer, KafkaError
import threading

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        dbname="reservation",
        user="postgres",
        password="secret",
        host="localhost"
    )

@app.route('/rooms', methods=['GET'])
def get_rooms():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM rooms")
    rooms = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": r[0], "name": r[1]} for r in rooms])

def kafka_consumer():
    consumer = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'salle-service',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe(['reservation-created'])
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f"Kafka error: {msg.error()}")
                break
        print(f"Received message: {msg.value().decode('utf-8')}")

if __name__ == '__main__':
    threading.Thread(target=kafka_consumer, daemon=True).start()
    app.run(host='0.0.0.0', port=5002)
