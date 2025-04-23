from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

# Database connection function
def get_db_connection():
    conn = psycopg2.connect(
        dbname="product_db", user="postgres", password="bc@asu", host="localhost", port="5432"
    )
    return conn

@app.route("/", methods=["GET", "POST"])
def index():
    search_results = []
    if request.method == "POST":
        keyword = request.form["keyword"]
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Full-text search query for the keyword
        cursor.execute("""
            SELECT * FROM products
            WHERE to_tsvector('english', name || ' ' || description) @@ to_tsquery('english', %s);
        """, (keyword,))
        
        search_results = cursor.fetchall()
        cursor.close()
        conn.close()
    
    return render_template("index.html", search_results=search_results)

if __name__ == "__main__":
    app.run(debug=True)
