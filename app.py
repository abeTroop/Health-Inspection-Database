from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        dbname="CSE412_Project", user="abrahamtroop", host="localhost", port="8888"
    )
    return conn

# Home Page
@app.route("/", methods=["GET", "POST"])
def index():
    search_results = []
    if request.method == "POST":
        keyword = request.form["keyword"]
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM facility
            WHERE to_tsvector('english', facility_name) @@ plainto_tsquery('english', %s);
        """, (keyword,))
        
        search_results = cursor.fetchall()
        cursor.close()
        conn.close()
    
    return render_template("index.html", search_results=search_results)

# Inspections Page
@app.route("/facility/<facility_id>", methods=["GET"])
def facility(facility_id):
    inspections = []
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM facility
        WHERE facility_id = %s;
    """, (facility_id,))

    facility = cursor.fetchone()

    cursor.execute("""
        SELECT * FROM inspection 
        WHERE facility_id = %s;
    """, (facility_id,))

    inspections = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("facility.html", facility=facility, inspections=inspections)

# Violations Page
@app.route("/inspection/<serial_number>", methods=["GET"])
def inspection(serial_number):
    violations = []
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM inspection
        WHERE serial_number = %s;
    """, (serial_number,))

    inspection = cursor.fetchone()

    cursor.execute("""
        SELECT * FROM violation 
        WHERE serial_number = %s;
    """, (serial_number,))

    violations = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("inspection.html", inspection=inspection, violations=violations)

if __name__ == "__main__":
    app.run(debug=True)
