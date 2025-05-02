from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2
import uuid

app = Flask(__name__)

# Session Secret Key
app.secret_key = "secret-key" # key for the login session for inspectors

def get_db_connection():
    conn = psycopg2.connect(
        dbname="CSE412_Project", user="postgres", password="newpassword", host="localhost", port="5432"
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

# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        employee_id = request.form["employee_id"]
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employee WHERE employee_id = %s;", (employee_id,))
        inspector = cursor.fetchone()
        cursor.close()
        conn.close()

        if inspector:
            session["employee_id"] = employee_id
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid Employee ID")
    
    return render_template("login.html")

#------------------------------Inspector Login for Add, Update, and Delete Violations ----------------------------------------------------

# Inspector Dashboard (page where inspectors can add, update, and delete violations)
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "employee_id" not in session:
        return redirect(url_for("login"))

    selected_serial = None
    violations = []

    if request.method == "POST":
        selected_serial = request.form.get("serial_number")

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if serial number exists in the inspection table
        cursor.execute("SELECT * FROM inspection WHERE serial_number = %s;", (selected_serial,))
        inspection_exists = cursor.fetchone()

        # Return table of violations if found, print message if not found
        if not inspection_exists:
            flash("Serial number not found")
            selected_serial = None  # reset
        else:
            cursor.execute("""
                SELECT * FROM violation
                WHERE serial_number = %s;
            """, (selected_serial,))
            violations = cursor.fetchall()

        cursor.close()
        conn.close()

    return render_template(
        "inspector_dashboard.html",
        employee_id=session["employee_id"],
        selected_serial=selected_serial,
        violations=violations
    )


# Add Violation 
@app.route("/violation/add/<serial_number>", methods=["GET", "POST"])
def add_violation(serial_number):
    if "employee_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        # Retrieves user inputs for the following info
        violation_code = request.form["violation_code"]
        violation_description = request.form["violation_description"]
        violation_status = request.form["violation_status"]
        points = int(request.form["points"])
        
        row_id = uuid.uuid4().hex[:13]  # Create a random unique row id

        conn = get_db_connection()
        cursor = conn.cursor()

        #Insert Query with new info
        cursor.execute("""
            INSERT INTO violation (row_id, violation_code, violation_description, violation_status, points, serial_number)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (row_id, violation_code, violation_description, violation_status, points, serial_number))
        conn.commit()
        cursor.close()
        conn.close()

        flash("Violation added successfully.")
        return redirect(url_for("dashboard"))

    return render_template("add_violation.html", serial_number=serial_number)

# Edit Violation
@app.route("/violation/edit/<row_id>", methods=["GET", "POST"])
def edit_violation(row_id):
    if "employee_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        # Retrieves user inputs for the following info
        violation_code = request.form["violation_code"]
        violation_description = request.form["violation_description"]
        violation_status = request.form["violation_status"]
        points = int(request.form["points"])

        # Update Query with new info
        cursor.execute("""
            UPDATE violation
            SET violation_code = %s, violation_description = %s, violation_status = %s, points = %s
            WHERE row_id = %s;
        """, (violation_code, violation_description, violation_status, points, row_id))
        conn.commit()
        cursor.close()
        conn.close()

        flash("Violation updated.")
        return redirect(url_for("dashboard"))

    cursor.execute("SELECT * FROM violation WHERE row_id = %s;", (row_id,))
    violation = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template("edit_violation.html", violation=violation)

# Delete Violation
@app.route("/violation/delete/<row_id>", methods=["POST"])
def delete_violation(row_id):
    if "employee_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM violation WHERE row_id = %s;", (row_id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Violation deleted.")
    return redirect(url_for("dashboard"))

# Logout 
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
# --------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
