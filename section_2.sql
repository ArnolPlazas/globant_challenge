/* Number of employees hired for each job and department in 2021 divided by quarter. The
table must be ordered alphabetically by department and job. */

SELECT
  d.department,
  j.job,
  COUNT(*) FILTER (WHERE EXTRACT(QUARTER FROM datetime::timestamp) = 1) AS Q1,
  COUNT(*) FILTER (WHERE EXTRACT(QUARTER FROM datetime::timestamp) = 2) AS Q2,
  COUNT(*) FILTER (WHERE EXTRACT(QUARTER FROM datetime::timestamp) = 3) AS Q3,
  COUNT(*) FILTER (WHERE EXTRACT(QUARTER FROM datetime::timestamp) = 4) AS Q4
FROM hired_employees h
INNER JOIN departments d ON h.department_id = d.id
INNER JOIN jobs j ON h.department_id = j.id
WHERE EXTRACT(YEAR FROM datetime::timestamp) = 2021
GROUP BY d.department, j.job
ORDER BY d.department, j.job

/* List of ids, name and number of employees hired of each department that hired more
employees than the mean of employees hired in 2021 for all the departments, ordered
by the number of employees hired (descending). */

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
select
  hpd.id,
  hpd.department,
  hpd.hired
FROM hires_per_dept hpd, avg_hires ah
WHERE hpd.hired > ah.avg_hired
ORDER BY hpd.hired;