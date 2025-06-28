import psycopg
from psycopg.rows import dict_row
from redis import Redis
from jose import jwt, JWTError
from datetime import datetime
from contextlib import contextmanager
import os


SECRET_KEY = "a4d8de3fba0162ceea84fd3c3b2169cbebb5b5ff09e314051d002f859e4173e4"
conn_str = os.environ["DATABASE_URL"]
redis_url = os.environ["REDIS_URL"]


@contextmanager
def connection():
    conn = psycopg.connect(conn_str, row_factory=dict_row)
    try:
        yield conn
    finally:
        conn.close()


@contextmanager
def redis_connection():
    try:
        r = Redis.from_url(redis_url)
        yield r
    finally:
        r.close()


def initialize_db():
    """
    Initializes the database by creating necessary tables if they do not exist.
    This function should be called once to set up the database schema.
    """
    with connection() as conn:
        users_table_query = """CREATE TABLE if not exists users (
                                id serial4 NOT NULL,
                                user_name text NOT NULL,
                                email_id text NOT NULL,
                                "password" text NOT NULL,
                                created_at timestamptz DEFAULT now() NULL,
                                CONSTRAINT users_pkey PRIMARY KEY (id)
                            );"""

        tasks_table_query = """CREATE TABLE if not exists tasks (
                                id serial4 NOT NULL,
                                title text NOT NULL,
                                description text NULL,
                                completed bool DEFAULT false NULL,
                                created_at timestamptz DEFAULT now() NULL,
                                updated_at timestamptz DEFAULT now() NULL,
                                userid int4 NULL,
                                CONSTRAINT tasks_pkey PRIMARY KEY (id),
                                CONSTRAINT tasks_users_fk FOREIGN KEY (userid) REFERENCES users(id)
                            );"""

        conn.execute(users_table_query)
        conn.execute(tasks_table_query)
        conn.commit()

        return {"message": "Database initialized successfully."}


async def generate_token(user_details):
    payload = {
        "username": user_details["user_name"],
        "login_at": datetime.now().isoformat(),
    }
    token = jwt.encode(payload, key=SECRET_KEY)

    return token


async def is_token_valid(token) -> bool:
    try:
        decrypted_token = jwt.decode(
            token,
            SECRET_KEY,
        )
        return True

    except JWTError:
        return False
