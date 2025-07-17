# Data-Migration-with-Python
🚀 SQL Server to PostgreSQL Data Migration with Python
This project is a production-grade data migration solution developed in Python to transfer a large-scale database from Microsoft SQL Server to PostgreSQL.

📌 Project Summary
Migrated millions of rows across multiple tables (e.g., Users, Moves, GameWords, FloodControl, etc.).

Ensured data type compatibility, including mapping SQL Server's INT, NVARCHAR(MAX), DATETIME, and BIT types to appropriate PostgreSQL types like INTEGER, TEXT, TIMESTAMP, and BOOLEAN.

Handled batch processing efficiently using optimized pagination (OFFSET and later key-based pagination with ID).

Included type transformation logic (e.g., converting integers like 0/1 to PostgreSQL-native booleans).

Logged migration progress with detailed output for traceability and debugging.

Addressed edge cases such as reserved keywords, naming mismatches, and missing fields.

🛠 Technologies
Python 3

pyodbc for SQL Server connection

psycopg2 for PostgreSQL connection

Logging module for real-time feedback

⚙️ Features
🔄 Batch-wise migration with configurable batch sizes

✅ Type-safe transformations (e.g., INT → BOOLEAN)

🧠 Intelligent error handling with rollback and recovery

📝 Auto-logging for every batch and table status

🔄 Schema mapping flexibility

📦 Use Case
This project was used in a real-world migration scenario where a company transitioned its backend from SQL Server to PostgreSQL while preserving data integrity, schema structure, and operational stability.
