
# 📘 Globant DB Migration API

This project provides a RESTful API using **FastAPI** to migrate, insert, and analyze HR data from CSV files into a PostgreSQL database. It supports both file-based ingestion and structured JSON batch ingestion for Departments, Jobs, and Hired Employees.

---

## 🚀 Base URL

```
http://localhost:8000
```

---

## 📂 Endpoints

### 📄 Data Retrieval Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/historical-department-data` | Get raw department data from CSV |
| GET    | `/historical-job-data`        | Get raw job data from CSV |
| GET    | `/historical-hired-employees-data` | Get raw hired employee data from CSV |

---

### 📤 File Upload Endpoints

These endpoints read predefined CSV files (`./data/*.csv`) and upsert data into PostgreSQL.

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/update-department` | Upload and upsert department data from CSV |
| POST   | `/update-job` | Upload and upsert job data from CSV |
| POST   | `/update-hired-employee` | Upload and upsert hired employee data from CSV |

> ⚠️ Only `.csv` files are allowed. Data is matched using the `id` as the unique key.

---

### 📦 Batch Insert Endpoints

Use these to send JSON-formatted data in bulk (up to 1000 items per request).

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/department/batch` | Insert or update a batch of departments |
| POST   | `/job/batch` | Insert or update a batch of jobs |
| POST   | `/hired-employees/batch` | Insert or update a batch of hired employees |

Example payload for `/department/batch`:

```json
[
  { "id": 1, "department": "Engineering" },
  { "id": 2, "department": "Marketing" }
]
```

---

### 📊 Analytical Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/hires/quarterly` | Returns quarterly hires per job and department for the year 2021 |
| GET    | `/hires/above-average` | Returns departments with above-average hires in 2021 |

---

## 🏗️ Project Structure

```
.
├── app/
│   ├── main.py                  # API entry point
│   ├── models.py                # SQLAlchemy models
│   ├── crud_sql.py              # DB interaction logic
│   ├── get_data_from_csv.py     # CSV parsing utilities
│   ├── schemas/                 # Pydantic schemas
├── data/                        # Sample CSV files
├── test/                        # Sample CSV files
├── Dockerfile
├── docker-compose.yml
```

---

## 🐳 Docker Setup


Create a .env file at the root with the following information

```bash
PGSUER=postgres
PGPASSWD=postgres
PGHOST=postgres
PGPORT=5432
PGDB=company_hr
```


### 1. Build and Start the Containers
Run the following command from the project root:

```bash
docker-compose up --build
```

This will:

- Start the FastAPI app on `http://localhost:8000`
- Start a PostgreSQL container on port `5432`
- Mount the project directory into the FastAPI container

### 2. Access the API

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 3. Stop the Containers

```bash
docker-compose down
```

---

### 🐘 PostgreSQL Credentials

- **Host**: `localhost`
- **Port**: `5432`
- **Database**: `postgres`
- **User**: `postgres`
- **Password**: `postgres`

---

## 🧪 Testing

```bash
pytest --cov=app
```
