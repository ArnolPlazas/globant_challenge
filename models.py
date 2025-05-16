from sqlalchemy import Column, Date, Integer, String, ForeignKey, MetaData
from sqlalchemy.orm import declarative_base

from connect_postgres import get_engine


SCHEMA = 'public'

Base = declarative_base(metadata=MetaData(schema=SCHEMA))
# engine = get_engine()


class HiredEmployee(Base):
    __tablename__ = 'hired_employees'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    datetime = Column(String(255), nullable=False)
    department_id = Column(Integer, ForeignKey('departments.id'))
    job_id = Column(Integer, ForeignKey('jobs.id'))


class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    department = Column(String(255), nullable=False)
    

class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    job = Column(String(255), nullable=False)