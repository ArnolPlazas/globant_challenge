import pandas as pd

from models import HiredEmployee, Department, Job
from connect_postgres import get_session

session = get_session()


def insert_data(path, columns, table):
    df = pd.read_csv(path, names=columns).convert_dtypes()
    list_dict = df.to_dict(orient='records')

    session.bulk_insert_mappings(table, list_dict)
    session.commit()
    session.close()

if __name__ == '__main__':
    insert_data('data/departments.csv', ['id', 'department'], Department)
    insert_data('data/jobs.csv', ['id', 'job'], Job)
    insert_data('data/hired_employees.csv', ['id', 'name', 'datetime', 'department_id', 'job_id'], HiredEmployee)