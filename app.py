from flask import *
import os
from database import engine, load_jobs_from_db, create_user, verify_user
from sqlalchemy import text

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-key-change-this")


@app.route("/")
def hello_world():
    jobs = load_jobs_from_db()
    return render_template("home.html", jobs=jobs)


@app.route('/apply/<int:job_id>')
def apply(job_id):
    jobs = load_jobs_from_db()
    job = next((item for item in jobs if item['id'] == job_id), None)
    if job is None:
        return 'Job not found', 404
    return render_template('job.html', job=job)


@app.route('/jobs')
def list_jobs():
    jobs = load_jobs_from_db()
    return jsonify(jobs)


@app.route("/signup", methods=["POST"])
def signup():
    data = request.form
    if data["password"] != data["confirm_password"]:
        return jsonify({"error": "Passwords do not match"}), 400

    success, error = create_user(data["name"], data["email"], data["password"])
    if not success:
        return jsonify({"error": error}), 400

    user = verify_user(data["email"], data["password"])
    session["user_id"] = user["id"]
    session["username"] = user["username"]
    return jsonify({"success": True})


@app.route("/login", methods=["POST"])
def login():
    data = request.form
    user = verify_user(data["email"], data["password"])
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401
    session["user_id"] = user["id"]
    session["username"] = user["username"]
    return jsonify({"success": True})


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("hello_world"))


if __name__ == '__main__':
    app.run(debug=True)