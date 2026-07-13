from sqlalchemy import create_engine, text

engine = create_engine(
    "mysql+pymysql://root:password@localhost:3306/jobs",
    connect_args={
        "ssl": {
            "ca": r"C:\Users\User\Downloads\ca (1).pem"
        }
    }
)


def load_jobs_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM jobs"))

        jobs = []

        for row in result.mappings():
            job = dict(row)

            # Convert responsibilities and requirements
            job["responsibilities"] = job["responsibilities"].split("\n")
            job["requirements"] = job["requirements"].split("\n")

            # Convert salary back to display format
            job["salary"] = f'{job["currency"]} {job["salary"]:,}'

            jobs.append(job)

        return jobs