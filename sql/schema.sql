PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    fio TEXT NOT NULL,
    department TEXT NOT NULL,
    age INTEGER NOT NULL CHECK (age BETWEEN 1 AND 120)
);

CREATE TABLE IF NOT EXISTS categories (
    code TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS statuses (
    code TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY,
    employee_id INTEGER NOT NULL,
    category_code TEXT NOT NULL,
    status_code TEXT NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees (id),
    FOREIGN KEY (category_code) REFERENCES categories (code),
    FOREIGN KEY (status_code) REFERENCES statuses (code)
);

CREATE INDEX IF NOT EXISTS idx_employees_department
    ON employees (department);
CREATE INDEX IF NOT EXISTS idx_requests_employee
    ON requests (employee_id);
CREATE INDEX IF NOT EXISTS idx_requests_category
    ON requests (category_code);
CREATE INDEX IF NOT EXISTS idx_requests_status
    ON requests (status_code);
