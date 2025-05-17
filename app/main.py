from typing import List
from fastapi import FastAPI, UploadFile, File, HTTPException
import os

from app.models import HiredEmployee, Department, Job
from app.schemas.department import DepartmentCreate
from app.schemas.job import JobCreate
from app.schemas.hired_employee import EmployeeCreate
from app.schemas.hire_stats import HireStats
from app.schemas.hire_quarter_stats import HireQuarterStats


from app.crud_sql import upsert_data, query_data
from app.get_data_from_csv import get_records_from_file


app = FastAPI(
    title="Globant DB Migration API",
    description="API for migrating data from CSV files to PostgreSQL database",
    version="1.0.0"
)

PATH_DEPARTMENT = './data/departments.csv'
COLUMNS_DEPARTMENT = ['id', 'department']

PATH_JOB = './data/jobs.csv'
COLUMNS_JOB = ['id', 'job']

PATH_HIREDEMPLOYEES = './data/hired_employees.csv'
COLUMNS_HIREDEMPLOYEES = ['id', 'name', 'datetime', 'department_id', 'job_id']

@app.get("/historical-department-data")
async def get_historical_department_data():
    if not os.path.exists(PATH_DEPARTMENT):
        raise HTTPException(status_code=404, detail="CSV file not found.")

    records = get_records_from_file(PATH_DEPARTMENT, COLUMNS_DEPARTMENT)

    return records


@app.get("/historical-job-data")
async def get_historical_department_data():
    if not os.path.exists(PATH_JOB):
        raise HTTPException(status_code=404, detail="CSV file not found.")
    
    records = get_records_from_file(PATH_JOB, COLUMNS_JOB)

    return records


@app.get("/historical-hired-employees-data")
async def get_historical_department_data():
    if not os.path.exists(PATH_HIREDEMPLOYEES):
        raise HTTPException(status_code=404, detail="CSV file not found.")
    
    records = get_records_from_file(PATH_HIREDEMPLOYEES, COLUMNS_HIREDEMPLOYEES)

    return records


@app.post("/update-department")
async def upsert_department_data(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")
    
    records = get_records_from_file(PATH_DEPARTMENT, COLUMNS_DEPARTMENT)

    try:
        upsert_data(model=Department, records=records, unique_constraint='id')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upsert failed: {e}")

    return {"message": f"Upserted {len(records)} users successfully."}


@app.post("/update-job")
async def upsert_job_data(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")
    
    records = get_records_from_file(PATH_JOB, COLUMNS_JOB)

    try:
        upsert_data(model=Job, records=records, unique_constraint='id')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upsert failed: {e}")

    return {"message": f"Upserted {len(records)} users successfully."}


@app.post("/update-hired-employee")
async def upsert_hired_employee_data(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")
    
    records = get_records_from_file(PATH_HIREDEMPLOYEES, COLUMNS_HIREDEMPLOYEES)

    try:
        upsert_data(model=HiredEmployee, records=records, unique_constraint='id')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upsert failed: {e}")

    return {"message": f"Upserted {len(records)} users successfully."}


@app.post("/department/batch")
def batch_upsert_departments(departments: List[DepartmentCreate]):
    if not 1 <= len(departments) <= 1000:
        raise HTTPException(status_code=400, detail="Batch size must be between 1 and 1000.")

    records = [department.model_dump() for department in departments]

    try:
        upsert_data(model=Department, records=records, unique_constraint='id')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upsert failed: {e}")

    return {"message": f"Upserted {len(records)} users successfully."}


@app.post("/job/batch")
def batch_upsert_jobs(jobs: List[JobCreate]):
    if not 1 <= len(jobs) <= 1000:
        raise HTTPException(status_code=400, detail="Batch size must be between 1 and 1000.")

    records = [job.model_dump() for job in jobs]

    try:
        upsert_data(model=Job, records=records, unique_constraint='id')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upsert failed: {e}")

    return {"message": f"Upserted {len(records)} users successfully."}


@app.post("/hired-employees/batch")
def batch_upsert_employees(employees: List[EmployeeCreate]):
    if not 1 <= len(employees) <= 1000:
        raise HTTPException(status_code=400, detail="Batch size must be between 1 and 1000.")

    records = [employee.model_dump() for employee in employees]

    try:
        upsert_data(model=HiredEmployee, records=records, unique_constraint='id')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upsert failed: {e}")

    return {"message": f"Upserted {len(records)} users successfully."}


@app.get("/hires/quarterly", response_model=List[HireQuarterStats])
def get_hires_by_quarter():
    query = """
        SELECT
          d.department,
          j.job,
          COUNT(*) FILTER (WHERE EXTRACT(QUARTER FROM h.datetime::timestamp) = 1) AS Q1,
          COUNT(*) FILTER (WHERE EXTRACT(QUARTER FROM h.datetime::timestamp) = 2) AS Q2,
          COUNT(*) FILTER (WHERE EXTRACT(QUARTER FROM h.datetime::timestamp) = 3) AS Q3,
          COUNT(*) FILTER (WHERE EXTRACT(QUARTER FROM h.datetime::timestamp) = 4) AS Q4
        FROM hired_employees h
        JOIN departments d ON h.department_id = d.id
        JOIN jobs j ON h.job_id = j.id
        WHERE EXTRACT(YEAR FROM h.datetime::timestamp) = 2021
        GROUP BY d.department, j.job
        ORDER BY d.department, j.job;
    """

    result = result = query_data(query)
    return [HireQuarterStats(department=r[0], job=r[1], Q1=r[2], Q2=r[3], Q3=r[4], Q4=r[5]) for r in result]



@app.get("/hires/above-average", response_model=List[HireStats])
def get_above_average_hires():
    query = """
        WITH hires_per_dept AS (
            SELECT
                d.id,
                d.department,
                COUNT(*) AS hired
            FROM hired_employees h
            JOIN departments d ON h.department_id = d.id
            WHERE EXTRACT(YEAR FROM h.datetime::timestamp) = 2021
            GROUP BY d.id, d.department
        ),
        avg_hires AS (
            SELECT AVG(hired) AS avg_hired FROM hires_per_dept
        )
        SELECT
            hpd.id,
            hpd.department,
            hpd.hired
        FROM hires_per_dept hpd, avg_hires ah
        WHERE hpd.hired > ah.avg_hired
        ORDER BY hpd.hired
    """

    result = query_data(query)

    return [HireStats(id=row[0], department=row[1], hired=row[2]) for row in result]