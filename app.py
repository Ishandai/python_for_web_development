from flask import *
from database import engine,load_jobs_from_db
from sqlalchemy import text
app = Flask(__name__)


@app.route("/")
def hello_world():

    jobs = load_jobs_from_db()

    return render_template(
        "home.html",
        jobs=jobs
    )


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


if __name__ == '__main__':
    app.run(debug=True)