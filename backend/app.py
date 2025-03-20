import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # ✅ Import CORS

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS for all routes

# ✅ Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:root@localhost:5432/crawler"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# ✅ Create folder to store uploaded files
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ✅ Define Database Model
class CrawlerConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crawling_depth = db.Column(db.Integer, nullable=False)
    max_pages = db.Column(db.Integer, nullable=False)
    concurrent_requests = db.Column(db.Integer, nullable=False)
    timeout_seconds = db.Column(db.Integer, nullable=False)
    selector = db.Column(db.String(255), nullable=False)
    csv_filename = db.Column(db.String(255), nullable=False)

# ✅ Create tables if not exist
with app.app_context():
    db.create_all()

# ✅ API to handle form submission
@app.route("/submit-crawler", methods=["POST"])
def submit_crawler():
    try:
        # Get form data
        form_data = request.form
        csv_file = request.files.get("csv_file")

        if not csv_file:
            return jsonify({"error": "CSV file is required"}), 400

        # Save the CSV file
        csv_filename = csv_file.filename
        csv_path = os.path.join(UPLOAD_FOLDER, csv_filename)
        csv_file.save(csv_path)

        # Store data in database
        new_entry = CrawlerConfig(
            crawling_depth=int(form_data["crawling_depth"]),
            max_pages=int(form_data["max_pages"]),
            concurrent_requests=int(form_data["concurrent_requests"]),
            timeout_seconds=int(form_data["timeout_seconds"]),
            selector=form_data["selector"],
            csv_filename=csv_filename
        )
        db.session.add(new_entry)
        db.session.commit()

        return jsonify({"message": "Data stored successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
