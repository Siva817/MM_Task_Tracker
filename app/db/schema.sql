-- MM Task Tracker - SQL Server Schema

-- Drop tables if they already exist
-- Only use this section when you want to recreate the database from scratch.

IF OBJECT_ID('dbo.tasks', 'U') IS NOT NULL
    DROP TABLE dbo.tasks;

IF OBJECT_ID('dbo.submissions', 'U') IS NOT NULL
    DROP TABLE dbo.submissions;

IF OBJECT_ID('dbo.managers', 'U') IS NOT NULL
    DROP TABLE dbo.managers;


-- Managers
CREATE TABLE managers (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(255) NOT NULL UNIQUE
);


-- Employee submissions
CREATE TABLE submissions (
    id INT IDENTITY(1,1) PRIMARY KEY,
    employee_id NVARCHAR(255),
    employee_name NVARCHAR(255),
    manager NVARCHAR(255),
    current_task NVARCHAR(500),
    idle BIT,
    drive_link NVARCHAR(1000),
    idle_remarks NVARCHAR(MAX),
    submitted_at DATETIME2
);


-- Tasks belonging to a submission
CREATE TABLE tasks (
    id INT IDENTITY(1,1) PRIMARY KEY,
    submission_id INT NOT NULL,
    task_id NVARCHAR(500),
    task_name NVARCHAR(1000),
    sway BIT,
    mm BIT,
    jobs NVARCHAR(255),
    remarks NVARCHAR(MAX),

    CONSTRAINT FK_tasks_submissions
        FOREIGN KEY (submission_id)
        REFERENCES submissions(id)
);
