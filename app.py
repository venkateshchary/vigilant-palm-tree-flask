import os
import psycopg2
import psycopg2.extras
 genre-apl


 main
from flask import Flask, jsonify, request

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST', 'db'),
        database=os.environ.get('POSTGRES_DB', 'chinook_auto_increment'),
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
        if db_version is None:
            return "<p>Error: no result from SELECT version()</p>"


    
        if db_version is None:
            return "<p>Error: no result from SELECT version()</p>"
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


@app.route("/album", methods=['GET'])
def get_album():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = 'select * from album'
        cur.execute(query)
        albums = cur.fetchall()  # list of dicts
        cur.close()
        conn.close()
        return jsonify(albums)
    except Exception as e:
        return f"<p>Error connecting to database: {e}</p>"
 
@app.route("/album/<int:album_id>", methods=['GET'])
def get_album_id(album_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute('SELECT * FROM album WHERE Album_ID = %s', (album_id,))
        albums = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(albums)
    except Exception as e:
        return f"<p>Error connecting to database: {e}</p>"

@app.route("/album/<int:album_id>", methods=['PUT'])
def update_albums(album_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        data = request.get_json()
        if not data or 'album_id' not in data:
            # Return a 400 Bad Request error if data is missing
            return jsonify({"error": "Missing 'album_id' in request body"}), 400
        else:
            cur.execute('UPDATE album SET title=%s WHERE Album_ID = %s',
                        (data['title'], album_id))
            conn.commit()
            cur.execute('SELECT * FROM album WHERE Album_ID = %s', (data['album_id'],))
            albums = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(albums)
    except Exception as e:
        return f"<p>Error connecting to database: {e}</p>"
    
@app.route("/artist", methods=['GET'])
def get_artist():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = 'select * from artist'
        cur.execute(query)
        artists = cur.fetchall()  # list of dicts
        cur.close()
        conn.close()
        return jsonify(artists)
    except Exception as e:
        return f"<p>Error connecting to database: {e}</p>"

@app.route("/artist/<int:artist_id>", methods=['GET'])
def get_artist_id(artist_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute('SELECT * FROM artist WHERE Artist_ID = %s', (artist_id,))
        artists = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(artists)
    except Exception as e:
        return f"<p>Error connecting to database: {e}</p>"

@app.route("/artist/<int:artist_id>", methods=['PUT'])
def update_artist(artist_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        data = request.get_json()
        if not data:
            # Return a 400 Bad Request error if data is missing
            return jsonify({"error": "Missing request body"}), 400
        else:
            cur.execute('UPDATE artist SET name=%s WHERE Artist_ID = %s',
                        (data['name'], artist_id))
            conn.commit()
            cur.execute('SELECT * FROM artist WHERE Artist_ID = %s', (artist_id,))
            artists = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(artists)
    except Exception as e:
        return f"<p>Error connecting to database: {e}</p>"
    
@app.route("/genre", methods=['GET'])
def get_genre():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = 'select * from genre'
        cur.execute(query)
        genres = cur.fetchall()  # list of dicts
        cur.close()
        conn.close()
        return jsonify(genres)
    except Exception as e:
        return f"<p>Error connecting to database: {e}</p>"

@app.route("/genre/<int:genre_id>", methods=['GET'])
def get_genre_id(genre_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute('SELECT * FROM genre WHERE Genre_ID = %s', (genre_id,))
        genres = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(genres)
    except Exception as e:
        return f"<p>Error connecting to database: {e}</p>"

@app.route("/genre/<int:genre_id>", methods=['PUT'])
def update_genre(genre_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        data = request.get_json()
        if not data:
            # Return a 400 Bad Request error if data is missing
            return jsonify({"error": "Missing request body"}), 400
        else:
            cur.execute('UPDATE genre SET name=%s WHERE Genre_ID = %s',
                        (data['name'], genre_id))
            conn.commit()
            cur.execute('SELECT * FROM genre WHERE Genre_ID = %s', (genre_id,))
            genres = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(genres)
    except Exception as e:
        return f"<p>Error connecting to database: {e}</p>"

@app.route("/invoice", methods=['GET'])
def get_invoice():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM invoice')
        invoices = cur.fetchall()
        cur.close()
        conn.close()
        return f"<p>Invoices: {invoices}</p>"
    except Exception as e:
        return f"<p>Error connecting to database: {e}</p>"

@app.route("/invoice/<string:invoice_id>", methods=['GET'])
def get_invoice_id(invoice_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM invoice WHERE Invoice_ID = %s', (invoice_id,))
        invoices = cur.fetchall()
        cur.close()
        conn.close()
        return f"<p>Invoices: {invoices}</p>"
    except Exception as e:
        return f"<p>Error connecting to database: {e}</p>"
    
'''
view all albums
@app.route("/albums", methods=['GET'])
view album by id
@app.route("/albums/<int:album_id>", methods=['GET'])
view all artists
@app.route("/artists", methods=['GET'])
view artist by id
@app.route("/artists/<int:artist_id>", methods=['GET'])
view all tracks
@app.route("/tracks", methods=['GET']) 
view track by id
@app.route("/tracks/<int:track_id>", methods=['GET'])
view all customers
@app.route("/customers", methods=['GET'])
view customer by id
@app.route("/customers/<int:customer_id>", methods=['GET'])
'''


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
