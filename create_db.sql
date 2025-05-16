
CREATE DATABASE company_hr;

create TABLE departments (
    id INTEGER PRIMARY KEY,
    department VARCHAR(255)
);

CREATE TABLE jobs (
    id INTEGER PRIMARY KEY,
    job VARCHAR(255)
);


CREATE TABLE hired_employees (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255),
    datetime VARCHAR(255),
    department_id INTEGER REFERENCES departments(id),
    job_id INTEGER REFERENCES jobs(id)
);