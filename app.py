import os
import psycopg2
from flask import Flask

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST', 'db'),
        database=os.environ.get('POSTGRES_DB', 'flaskdb'),
        user=os.environ.get('POSTGRES_USER', 'user'),
        password=os.environ.get('POSTGRES_PASSWORD', 'password')
    )
    return conn

@app.route("/")
def hello_world():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        cur.close()
        conn.close()
        return f"<p>Hello, World! Connected to: {db_version[0]}</p>"
    except Exception as e:
        return f"<p>Error connecting to database: {e}</p>"


@app.route("/employees", methods=['GET'])
def get_employees():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM employee')
        employees = cur.fetchall()
        cur.close()
        conn.close()
        return f"<p>Employees: {employees}</p>"
    except Exception as e:
        return f"<p>Error connecting to database: {e}</p>"

@app.route("/employees/<string:emp_id>", methods=['GET'])
def get_employee(emp_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM employee WHERE Emp_ID = %s', (emp_id,))
        employee = cur.fetchone()
        cur.close()
        conn.close()
        return f"<p>Employee: {employee}</p>"
    except Exception as e:
        return f"<p>Error connecting to database: {e}</p>"




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
