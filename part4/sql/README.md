# SQL Scripts for Holberton BnB Project

This directory contains SQL scripts used for managing the database schema and testing CRUD operations for the Holberton HBnB project.

## Files

- `hbnb_schema.sql`: This script contains the SQL commands to create the database schema, including tables, relationships, and constraints necessary for the Holberton HBnB application.

- `hbnb_crud_test.sql`: This script is designed to test CRUD (Create, Read, Update, Delete) operations on the database. It includes sample SQL statements to insert, select, update, and delete data to verify that the schema works as expected.

## Usage

1. To create the database schema, run the `hbnb_schema.sql` script on your SQL server. For example, using MySQL:

   ```bash
   mysql -u username -p < hbnb_schema.sql
   ```

2. After the schema is created, you can use the `hbnb_crud_test.sql` script to test the CRUD operations:

   ```bash
   mysql -u username -p < hbnb_crud_test.sql
   ```

Replace `username` with your actual database username. You will be prompted to enter your password.

Make sure your database server is running and accessible before executing these scripts.
