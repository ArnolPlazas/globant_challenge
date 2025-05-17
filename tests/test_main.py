import io
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app

client = TestClient(app)

# Mock data
mock_departments = [{"id": 1, "department": "HR"}]
mock_jobs = [{"id": 1, "job": "Engineer"}]
mock_employees = [{"id": 1, "name": "John", "datetime": "2021-01-01", "department_id": 1, "job_id": 1}]
mock_stats = [("Engineering", "Sales", 5, 2, 3, 1)]
mock_above_avg = [(1, "Engineering", 10)]

# ---- GET Historical ----

@patch("app.main.get_records_from_file", return_value=mock_departments)
@patch("app.main.os.path.exists", return_value=True)
def test_get_historical_department_data(_, __):
    response = client.get("/historical-department-data")
    assert response.status_code == 200
    assert response.json() == mock_departments

@patch("app.main.get_records_from_file", return_value=mock_jobs)
@patch("app.main.os.path.exists", return_value=True)
def test_get_historical_job_data(_, __):
    response = client.get("/historical-job-data")
    assert response.status_code == 200
    assert response.json() == mock_jobs

@patch("app.main.get_records_from_file", return_value=mock_employees)
@patch("app.main.os.path.exists", return_value=True)
def test_get_historical_hired_employees_data(_, __):
    response = client.get("/historical-hired-employees-data")
    assert response.status_code == 200
    assert response.json() == mock_employees

# ---- Error cases for GET ----

@patch("app.main.os.path.exists", return_value=False)
def test_csv_not_found(mock_exists):
    response = client.get("/historical-department-data")
    assert response.status_code == 404

# ---- POST file upserts ----

@patch("app.main.get_records_from_file", return_value=[{"id": 1, "department": "Engineering"}])
@patch("app.main.upsert_data")
def test_upsert_department_data_success(mock_upsert, mock_get_records):
    file_content = "id,department\n1,Engineering\n"
    response = client.post(
        "/update-department",
        files={"file": ("departments.csv", io.BytesIO(file_content.encode("utf-8")), "text/csv")}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Upserted 1 users successfully."}
    mock_get_records.assert_called_once()
    mock_upsert.assert_called_once()


@patch("app.main.get_records_from_file", return_value=[{"id": 1, "job": "Data Engineer"}])
@patch("app.main.upsert_data")
def test_upsert_job_data_success(mock_upsert, mock_get_records):
    file_content = "id,job\n1,Data Engineer\n"
    response = client.post(
        "/update-job",
        files={"file": ("jobs.csv", io.BytesIO(file_content.encode("utf-8")), "text/csv")}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Upserted 1 users successfully."}
    mock_get_records.assert_called_once()
    mock_upsert.assert_called_once()


@patch("app.main.get_records_from_file", return_value=[{
    "id": 1, "name": "Alice", "datetime": "2021-01-01 10:00:00", "department_id": 1, "job_id": 1
}])
@patch("app.main.upsert_data")
def test_upsert_hired_employee_data_success(mock_upsert, mock_get_records):
    file_content = "id,name,datetime,department_id,job_id\n1,Alice,2021-01-01 10:00:00,1,1\n"
    response = client.post(
        "/update-hired-employee",
        files={"file": ("hired_employees.csv", io.BytesIO(file_content.encode()), "text/csv")}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Upserted 1 users successfully."}
    mock_get_records.assert_called_once()
    mock_upsert.assert_called_once()


# ---- POST batch upserts ----

@patch("app.main.upsert_data")
def test_batch_upsert_departments(mock_upsert):
    response = client.post("/department/batch", json=[{"id": 1, "department": "HR"}])
    assert response.status_code == 200

@patch("app.main.upsert_data")
def test_batch_upsert_limit(mock_upsert):
    data = [{"id": i, "department": "D"} for i in range(1001)]
    response = client.post("/department/batch", json=data)
    assert response.status_code == 400

# ---- Analytical Endpoints ----

@patch("app.main.query_data", return_value=mock_stats)
def test_get_hires_by_quarter(mock_query):
    response = client.get("/hires/quarterly")
    assert response.status_code == 200
    assert response.json()[0]["department"] == "Engineering"

@patch("app.main.query_data", return_value=mock_above_avg)
def test_get_above_average_hires(mock_query):
    response = client.get("/hires/above-average")
    assert response.status_code == 200
    assert response.json()[0]["department"] == "Engineering"