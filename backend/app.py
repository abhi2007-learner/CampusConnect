from flask import Flask,jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def create_database():
    conn = sqlite3.connect("campusconnect.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT
        )
    """)
    cursor.execute("""
    INSERT OR IGNORE INTO events
    (id, title, date, description)
    VALUES
    (1, 'Tech Fest 2026', '2026-09-15',
     'A college technical festival with coding and project events.')
""")

    cursor.execute("""
    INSERT OR IGNORE INTO events
    (id, title, date, description)
    VALUES
    (2, 'Cultural Night', '2026-09-20',
     'An evening celebrating music, dance and culture.')
""")

    cursor.execute("""
    INSERT OR IGNORE INTO events
    (id, title, date, description)
    VALUES
    (3, 'Annual Sports Meet', '2026-09-25',
     'Annual college sports competition.')
""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        date TEXT NOT NULL
    )
""")
    cursor.execute("""
    INSERT OR IGNORE INTO notices (id, title, content, date)
    VALUES
    (1, 'Exam Schedule Released',
     'The semester examination schedule has been released.',
     '2026-09-10')
""")

    cursor.execute("""
    INSERT OR IGNORE INTO notices (id, title, content, date)
    VALUES
    (2, 'Campus Cleanliness Drive',
     'Students are invited to participate in the campus cleanliness drive.',
     '2026-09-12')
""")

    cursor.execute("""
    INSERT OR IGNORE INTO notices (id, title, content, date)
    VALUES
    (3, 'Hackathon Registration Open',
     'Registration is now open for the upcoming college hackathon.',
     '2026-09-15')
""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_id INTEGER NOT NULL,
        student_name TEXT NOT NULL,
        student_email TEXT NOT NULL
    )
""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            course TEXT,
            year TEXT,
            bio TEXT
        )
    """)
    
    cursor.execute("""
        INSERT OR IGNORE INTO profile
        (id, name, email, course, year, bio)
        VALUES
        (1, 'Abhishikta', 'hi@gmail.com',
         'Computer Science', '2nd Year',
         'CSE student at CampusConnect')
    """)
    cursor.execute("""
    UPDATE profile
    SET email = 'hi@gmail.com',
        course = 'Computer Science & Engineering',
        year = 'Second Year'
    WHERE id = 1
""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS community_posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        author TEXT NOT NULL,
        content TEXT NOT NULL,
        date TEXT NOT NULL,
        likes INTEGER DEFAULT 0
    )
""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER NOT NULL,
        author TEXT NOT NULL,
        content TEXT NOT NULL,
        date TEXT NOT NULL
    )
""")
    cursor.execute("""
    INSERT INTO community_posts (author, content, date)
    SELECT 'Abhishikta', 'Welcome to CampusConnect Community! 🎓', '2026-09-05'
    WHERE NOT EXISTS (
        SELECT 1 FROM community_posts
    )
""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
""")

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return "CampusConnect Backend is Running!"

@app.route("/api/notices")
def get_notices():
    conn = sqlite3.connect("campusconnect.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM notices")
    notices = cursor.fetchall()

    conn.close()

    return jsonify([dict(notice) for notice in notices])
@app.route("/api/admin/notices", methods=["POST"])
def add_notice():
    data = request.get_json()

    title = data.get("title")
    content = data.get("content")
    date = data.get("date")

    if not title or not content or not date:
        return jsonify({"message": "All fields are required"}), 400

    conn = sqlite3.connect("campusconnect.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO notices (title, content, date)
        VALUES (?, ?, ?)
    """, (title, content, date))

    conn.commit()
    conn.close()

    return jsonify({"message": "Notice added successfully!"})
@app.route("/api/notifications")
def get_notifications():
    conn = sqlite3.connect("campusconnect.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, content, date, 'notice' AS type
        FROM notices
        ORDER BY date DESC
    """)

    notifications = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return jsonify(notifications)

@app.route("/api/profile")
def get_profile():
    email = request.args.get("email")

    if not email:
        return jsonify({"message": "Email is required"}), 400

    conn = sqlite3.connect("campusconnect.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        users.name,
        users.email,
        profile.course,
        profile.year,
        profile.bio
    FROM users
    LEFT JOIN profile ON users.email = profile.email
    WHERE users.email = ?
""", (email,))

    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify(dict(user))

    return jsonify({"message": "User not found"}), 404
@app.route("/api/profile", methods=["PUT"])
def update_profile():
    data = request.get_json()

    email = data.get("email")
    course = data.get("course")
    year = data.get("year")
    bio = data.get("bio")

    if not email:
        return jsonify({"message": "Email is required"}), 400

    conn = sqlite3.connect("campusconnect.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE profile
        SET course = ?, year = ?, bio = ?
        WHERE email = ?
    """, (course, year, bio, email))

    conn.commit()
    conn.close()

    return jsonify({"message": "Profile updated successfully!"})

@app.route("/api/events")
def get_events():
    conn = sqlite3.connect("campusconnect.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()

    conn.close()

    return jsonify([dict(event) for event in events])
@app.route("/api/admin/events", methods=["POST"])
def add_event():
    data = request.get_json()

    title = data.get("title")
    description = data.get("description")
    date = data.get("date")

    if not title or not description or not date:
        return jsonify({"message": "All fields are required"}), 400

    conn = sqlite3.connect("campusconnect.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO events (title, date, description)
        VALUES (?, ?, ?)
    """, (title, date, description))

    conn.commit()
    conn.close()

    return jsonify({"message": "Event added successfully!"})


@app.route("/api/register", methods=["POST"])
def register_event():
    data = request.get_json()

    event_id = data["event_id"]
    student_name = data["student_name"]
    student_email = data["student_email"]

    conn = sqlite3.connect("campusconnect.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO registrations
        (event_id, student_name, student_email)
        VALUES (?, ?, ?)
    """, (event_id, student_name, student_email))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Registration successful!"
    })
@app.route("/api/community", methods=["GET"])
def get_community_posts():
    conn = sqlite3.connect("campusconnect.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM community_posts ORDER BY id DESC")
    posts = cursor.fetchall()

    conn.close()

    return jsonify([dict(post) for post in posts])


@app.route("/api/community", methods=["POST"])
def create_community_post():
    data = request.get_json()

    author = data.get("author")
    content = data.get("content")
    date = data.get("date")

    if not author or not content or not date:
        return jsonify({"message": "All fields are required"}), 400

    conn = sqlite3.connect("campusconnect.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO community_posts (author, content, date)
        VALUES (?, ?, ?)
    """, (author, content, date))

    conn.commit()
    conn.close()

    return jsonify({"message": "Post created successfully!"}), 201

@app.route("/api/comments", methods=["POST"])
def create_comment():
    data = request.get_json()

    post_id = data.get("post_id")
    author = data.get("author")
    content = data.get("content")
    date = data.get("date")

    if not post_id or not author or not content or not date:
        return jsonify({"message": "All fields are required"}), 400

    conn = sqlite3.connect("campusconnect.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO comments (post_id, author, content, date)
        VALUES (?, ?, ?, ?)
    """, (post_id, author, content, date))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Comment added successfully!"
    }), 201
@app.route("/api/comments/<int:post_id>", methods=["GET"])
def get_comments(post_id):
    conn = sqlite3.connect("campusconnect.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM comments
        WHERE post_id = ?
        ORDER BY id ASC
    """, (post_id,))

    comments = cursor.fetchall()
    conn.close()

    return jsonify([dict(comment) for comment in comments])

@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"message": "All fields are required"}), 400

    conn = sqlite3.connect("campusconnect.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (name, email, password)
            VALUES (?, ?, ?)
        """, (name, email, password))

        conn.commit()

    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"message": "Email already registered"}), 400

    conn.close()

    return jsonify({
        "message": "Signup successful!"
    }), 201
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    conn = sqlite3.connect("campusconnect.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email = ? AND password = ?",
        (email, password)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({
            "message": "Login successful!",
            "name": user["name"]
        })

    return jsonify({
        "message": "Invalid email or password"
    }), 401

if __name__ == "__main__":
    create_database()
    app.run(debug=True)
