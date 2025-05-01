from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        dbname="cse412_project", user="postgres", password="temp", host="localhost", port="5432"
        # insert password
    )
    return conn

# Home Page
@app.route("/", methods=["GET", "POST"])
def index():
    search_results = []
    if request.method == "POST":
        keyword = request.form["keyword"]
        address = request.form["address"]
        zip = request.form["zip"]
        city = request.form["city"]
        state = request.form["state"]

        conn = get_db_connection()
        cursor = conn.cursor()
        
        if not keyword and not address and not zip and not city and not state:
            # No input provided — skip DB query
            return render_template("index.html", search_results=[])


        query = "SELECT * FROM facility WHERE "
        params = []

        conditions = []
        if keyword:
            conditions.append("to_tsvector('english', facility_name) @@ plainto_tsquery('english', %s)")
            params.append(keyword)
        if address:
            conditions.append("to_tsvector('english', facility_address) @@ plainto_tsquery('english', %s)")
            params.append(address)
        if zip:
            conditions.append("to_tsvector('english', facility_zip) @@ plainto_tsquery('english', %s)")
            params.append(zip)
        if city:
            conditions.append("to_tsvector('english', facility_city) @@ plainto_tsquery('english', %s)")
            params.append(city)
        if state:
            conditions.append("to_tsvector('english', facility_state) @@ plainto_tsquery('english', %s)")
            params.append(state)

        query += " AND ".join(conditions)

        cursor.execute(query, tuple(params))

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
