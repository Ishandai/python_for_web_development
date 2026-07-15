from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text, create_engine
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os
from flask_login import UserMixin

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

# --- User model wrapping a DB row, required by flask-login ---
class User(UserMixin):
    def __init__(self, id, username, email, password_hash):
        self.id = str(id)          # flask-login expects get_id() to return a string
        self.username = username
        self.email = email
        self.password_hash = password_hash

    @staticmethod
    def from_row(row):
        if not row:
            return None
        return User(row["id"], row["username"], row["email"], row["password_hash"])


def create_user(username, email, password):
    password_hash = generate_password_hash(password)
    with engine.connect() as conn:
        try:
            conn.execute(
                text("INSERT INTO users (username, email, password_hash) VALUES (:u, :e, :p)"),
                {"u": username, "e": email, "p": password_hash}
            )
            conn.commit()
            return True, None
        except IntegrityError:
            return False, "Email already registered"


def get_user_by_id(user_id):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users WHERE id = :id"), {"id": user_id})
        return User.from_row(result.mappings().first())


def get_user_by_email(email):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users WHERE email = :e"), {"e": email})
        return User.from_row(result.mappings().first())


def verify_user(email, password):
    user = get_user_by_email(email)
    if user and check_password_hash(user.password_hash, password):
        return user
    return None