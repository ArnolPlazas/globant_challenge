import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

def get_engine():
    user = os.getenv('PGSUER')
    passwd = os.getenv('PGPASSWD')
    host = os.getenv('PGHOST')
    port = os.getenv('PGPORT')
    db = os.getenv('PGDB')

    url = f'postgresql://{user}:{passwd}@{host}:{port}/{db}'
    engine = create_engine(url, pool_size=50, echo=False)
    return engine


def get_session():
    engine = get_engine()
    session = sessionmaker(bind=engine)()
    return session

