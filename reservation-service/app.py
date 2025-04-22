from flask import Flask, jsonify, request
import psycopg2
from confluent_kafka import Producer

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        dbname="reservation",
        user="postgres",
        password="secret",
        host="localhost"
    )

producer = Producer({'bootstrap.servers': 'localhost:9092'})

@app.route('/reservations', methods=['POST'])
def create_reservation():
    data = request.json
    room_id = data.get('room_id')
    user_id = data.get('user_id')
    start_time = data.get('start_time')

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO reservations (room_id, user_id, start_time) VALUES (%s, %s, %s) RETURNING id",
        (room_id, user_id, start_time)
    )
    reservation_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    # Publish to Kafka
    reservation = f"Reservation: id={reservation_id}, room_id={room_id}, user_id={user_id}, start_time={start_time}"
    producer.produce('reservation-created', value=reservation.encode('utf-8'))
    producer.flush()

    return jsonify({"message": "Reservation created", "id": reservation_id}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
