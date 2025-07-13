from flask import Flask, render_template, request, redirect
import mysql.connector
from config import DB_CONFIG

app = Flask(__name__)

# Connect to MySQL
db = mysql.connector.connect(
    host=DB_CONFIG['host'],
    user=DB_CONFIG['user'],
    password=DB_CONFIG['password'],
    database=DB_CONFIG['database']
)
cursor = db.cursor()

# 🔹 Redirect root to /add-review
@app.route('/')
def home():
    return redirect('/add-review')

# Route to add a review
@app.route('/add-review', methods=['GET', 'POST'])
def add_review():
    if request.method == 'POST':
        school = request.form['school_name']
        reviewer = request.form['reviewer_name']
        rating = request.form['rating']

        sql = "INSERT INTO reviews (school_name, reviewer_name, rating) VALUES (%s, %s, %s)"
        val = (school, reviewer, rating)
        cursor.execute(sql, val)
        db.commit()

        return redirect('/reviews')

    return render_template('add_review.html')

# Route to display all reviews
@app.route('/reviews')
def show_reviews():
    cursor.execute("SELECT school_name, reviewer_name, rating FROM reviews ORDER BY id DESC")
    reviews = cursor.fetchall()
    return render_template('reviews.html', reviews=reviews)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
