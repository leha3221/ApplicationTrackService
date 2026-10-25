-- Lists of domain objects

-- name: employee_list
SELECT id, fio, department, age
FROM employees
ORDER BY fio;

-- name: request_list
SELECT
    r.id,
    r.employee_id,
    e.fio AS employee_fio,
    e.department,
    c.name AS type,
    s.name AS status,
    r.date
FROM requests AS r
JOIN employees AS e ON e.id = r.employee_id
JOIN categories AS c ON c.code = r.category_code
JOIN statuses AS s ON s.code = r.status_code
ORDER BY r.date DESC, r.id DESC;

-- Filters with bound values

-- name: employee_search
SELECT id, fio, department, age
FROM employees
WHERE casefold(fio) LIKE '%' || casefold(?) || '%'
   OR casefold(department) LIKE '%' || casefold(?) || '%'
ORDER BY fio;

-- name: request_search
SELECT
    r.id,
    r.employee_id,
    e.fio AS employee_fio,
    e.department,
    c.name AS type,
    s.name AS status,
    r.date
FROM requests AS r
JOIN employees AS e ON e.id = r.employee_id
JOIN categories AS c ON c.code = r.category_code
JOIN statuses AS s ON s.code = r.status_code
WHERE casefold(e.fio) LIKE '%' || casefold(?) || '%'
   OR casefold(c.name) LIKE '%' || casefold(?) || '%'
   OR casefold(s.name) LIKE '%' || casefold(?) || '%'
ORDER BY r.date DESC, r.id DESC;

-- Details and related domain data

-- name: employee_detail
SELECT id, fio, department, age
FROM employees
WHERE id = ?;

-- name: employee_requests
SELECT
    r.id,
    r.employee_id,
    e.fio AS employee_fio,
    e.department,
    c.name AS type,
    s.name AS status,
    r.date
FROM requests AS r
JOIN employees AS e ON e.id = r.employee_id
JOIN categories AS c ON c.code = r.category_code
JOIN statuses AS s ON s.code = r.status_code
WHERE r.employee_id = ?
ORDER BY r.date DESC, r.id DESC;

-- name: request_detail
SELECT
    r.id,
    r.employee_id,
    e.fio AS employee_fio,
    e.department,
    e.age AS employee_age,
    c.name AS type,
    s.name AS status,
    r.date
FROM requests AS r
JOIN employees AS e ON e.id = r.employee_id
JOIN categories AS c ON c.code = r.category_code
JOIN statuses AS s ON s.code = r.status_code
WHERE r.id = ?;

-- Aggregates and grouped reports

-- name: dashboard_counts
SELECT
    (SELECT COUNT(*) FROM employees) AS employees_count,
    (SELECT COUNT(*) FROM requests) AS requests_count;

-- name: request_counts_by_category
SELECT c.code, c.name AS type, COUNT(r.id) AS request_count
FROM categories AS c
LEFT JOIN requests AS r ON r.category_code = c.code
GROUP BY c.code, c.name
ORDER BY request_count DESC, c.name;

-- name: request_counts_by_status
SELECT s.code, s.name AS status, COUNT(r.id) AS request_count
FROM statuses AS s
LEFT JOIN requests AS r ON r.status_code = s.code
GROUP BY s.code, s.name
ORDER BY request_count DESC, s.name;

-- name: employee_counts_by_department
SELECT department, COUNT(*) AS employee_count, AVG(age) AS average_age
FROM employees
GROUP BY department
ORDER BY employee_count DESC, department;

-- name: request_counts_by_department
SELECT e.department, COUNT(r.id) AS request_count
FROM employees AS e
LEFT JOIN requests AS r ON r.employee_id = e.id
GROUP BY e.department
ORDER BY request_count DESC, e.department;

-- name: departments_above_request_count
SELECT e.department, COUNT(r.id) AS request_count
FROM employees AS e
JOIN requests AS r ON r.employee_id = e.id
GROUP BY e.department
HAVING COUNT(r.id) > ?
ORDER BY request_count DESC, e.department;
