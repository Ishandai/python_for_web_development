import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


load_dotenv()

mysql_user = os.getenv("MYSQL_USER")
mysql_password = os.getenv("MYSQL_PASSWORD")
mysql_host = os.getenv("MYSQL_HOST")
mysql_port = os.getenv("MYSQL_PORT")
mysql_database = os.getenv("MYSQL_DATABASE")
mysql_ssl_ca = os.getenv("MYSQL_SSL_CA")

if not all([mysql_user, mysql_password, mysql_host, mysql_port, mysql_database, mysql_ssl_ca]):
    raise RuntimeError("Missing one or more MySQL environment variables in .env")

engine = create_engine(
    f"mysql+pymysql://{quote_plus(mysql_user)}:{quote_plus(mysql_password)}@{mysql_host}:{mysql_port}/{mysql_database}",
    connect_args={
        "ssl": {
            "ca": mysql_ssl_ca
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