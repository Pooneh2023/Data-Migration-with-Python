##🛠️ Data-Migration-with-Python
🚀 SQL Server to PostgreSQL Data Migration Tool
This project is a production-grade Python script designed to migrate large-scale relational data from Microsoft SQL Server to PostgreSQL reliably, efficiently, and with full logging and error handling.

📌 Project Summary
Migrated millions of rows across multiple tables (e.g., Users, Moves, GameWords, FloodControl, etc.).

Ensured data type compatibility, converting types like:

INT → INTEGER

NVARCHAR(MAX) → TEXT

DATETIME → TIMESTAMP

BIT → BOOLEAN

Performed batch-wise data transfer using optimized pagination via OFFSET (with potential for key-based pagination later).

Included data transformation logic, such as converting 0/1 to native PostgreSQL booleans.

Implemented detailed logging for traceability, error reporting, and performance tracking.

Handled edge cases like naming mismatches, reserved keywords, and missing/null values.

🧰 Technologies Used
Python 3

pyodbc – for SQL Server connection

psycopg2 – for PostgreSQL connection

logging – for real-time feedback and file-based logs

⚙️ Key Features
Feature	Description
🔄 Batch Processing	Customizable batch sizes for standard and large tables
✅ Type-safe Transformation	Automatically converts INT to BOOLEAN and other type adjustments
🧠 Error Handling & Recovery	Rolls back transactions on failure to maintain data integrity
📝 Auto Logging	Logs every batch, table, and error with timestamps
🔧 Schema-Agnostic	Dynamically detects columns and adjusts inserts to fit destination schema

📦 Real-World Use Case
This script was deployed in a real-world scenario where an organization migrated its backend from SQL Server to PostgreSQL. The migration preserved:

Full data integrity

Field types and structure

Operational continuity with minimal downtime

🚧 Setup & Usage
Fill in the configuration section:

SQL Server and PostgreSQL connection details

Tables to migrate

Batch size preferences

Run the script:

bash
Copy
Edit
python3 migrate.py
Check logs via migration.log for progress and results.
