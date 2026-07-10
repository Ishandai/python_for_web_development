from flask import *

app = Flask(__name__)

JOBS = [
    {
        'id': 1,
        'title': 'Data Analyst',
        'location': 'New York, NY',
        'salary': '$120,000',
        'description': 'Turn raw business data into clear insights that support product, finance, and leadership decisions.',
        'responsibilities': [
            'Build dashboards and recurring reports',
            'Analyze trends and explain performance shifts',
            'Partner with teams to define key metrics'
        ],
        'requirements': [
            'Strong SQL and spreadsheet skills',
            'Experience with BI tools',
            'Clear communication and problem solving'
        ]
    },
    {
        'id': 2,
        'title': 'Data Scientist',
        'location': 'San Francisco, CA',
        'salary': '$150,000',
        'description': 'Design experiments and modeling workflows that help the business make better predictions and decisions.',
        'responsibilities': [
            'Develop and evaluate machine learning models',
            'Run experiments and interpret results',
            'Collaborate with engineering and product teams'
        ],
        'requirements': [
            'Python and statistical modeling experience',
            'Familiarity with ML frameworks',
            'Ability to explain complex findings simply'
        ]
    },
    {
        'id': 3,
        'title': 'Frontend Engineer',
        'location': 'Remote',
        'salary': '$130,000',
        'description': 'Craft fast, polished user interfaces that feel seamless across desktop and mobile.',
        'responsibilities': [
            'Build responsive UI components',
            'Work closely with design and product',
            'Improve performance and accessibility'
        ],
        'requirements': [
            'Strong HTML, CSS, and JavaScript skills',
            'Experience with component-based UI',
            'Attention to detail in visual design'
        ]
    },
    {
        'id': 4,
        'title': 'Backend Engineer',
        'location': 'Austin, TX',
        'salary': '$140,000',
        'description': 'Build reliable APIs and backend systems that keep the platform fast, stable, and secure.',
        'responsibilities': [
            'Design API endpoints and business logic',
            'Manage data storage and integrations',
            'Improve system reliability and observability'
        ],
        'requirements': [
            'Experience with web frameworks and APIs',
            'Strong debugging and architecture skills',
            'Comfort working with databases'
        ]
    },
  
]

@app.route('/')
def hello_world():
    return render_template('home.html', jobs=JOBS)

@app.route('/apply/<int:job_id>')
def apply(job_id):
    job = next((item for item in JOBS if item['id'] == job_id), None)
    if job is None:
        return 'Job not found', 404
    return render_template('job.html', job=job)

@app.route('/jobs')
def list_jobs():
    return jsonify(JOBS)


if __name__ == '__main__':
    app.run(debug=True)