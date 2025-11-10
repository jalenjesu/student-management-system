DROP TABLE IF EXISTS students;

-- Create students table with proper schema
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    enrollment_date DATE NOT NULL
);

-- Insert initial data
INSERT INTO students (first_name, last_name, email, enrollment_date) 
VALUES
    ('John', 'Doe', 'john.doe@example.com', '2023-09-01'),
    ('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
    ('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02');

-- Show the results
SELECT * FROM students;