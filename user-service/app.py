from flask import Flask, jsonify

import psycopg2


app = Flask(__name__)


def get_db_connection():

    return psycopg2.connect(

        dbname="reservation",

        user="postgres",

        password="secret",

        host="localhost"

    )


@app.route('/users', methods=['GET'])

def get_users():

    conn = get_db_connection()

    cur = conn.cursor()

    cur.execute("SELECT id, email FROM users")

    users = cur.fetchall()

    cur.close()

    conn.close()

    return jsonify([{"id": u[0], "email": u[1]} for u in users])


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5001) 
