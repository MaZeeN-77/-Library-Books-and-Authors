# Library and To-Do Application

Author: Mazen Ibrahim

Student ID: 2304122

A web application with two parts: a to-do list with user accounts, and a small library of authors and books.

## Features

To-Do:
- Register, log in and log out
- Add, edit, mark as done and delete tasks
- Each user sees only their own tasks
- Passwords are stored hashed
- Form validation with error messages

Library:
- Show a table of books and a table of authors
- Add a book and add an author
- Edit a book and edit an author
- Remove a book and remove an author
- Removing an author also removes all of that author's books

## Technologies

- Python (Flask)
- SQL Server with pyodbc
- bcrypt
- python-dotenv
- HTML and CSS

## Project Structure

    lab3-2304122/
        problem1_DDL.sql
        problem1_DML.sql
        problem1_Answers.txt
        problem2_DDL.sql
        problem2_DML.sql
        README.md
        website/
            app.py
            db.py
            requirements.txt
            .env.example
            database/
            templates/
            static/

## SQL Files

- problem1_DDL.sql, problem1_DML.sql: COMPANY database schema and data
- problem1_Answers.txt: answers to Q1.1 to Q1.3
- problem2_DDL.sql, problem2_DML.sql: library database schema and seed data

The SQL files are written for SQL Server.

## How to Run

1. In SSMS, run the script inside `website/database/` (To-Do database), then `problem2_DDL.sql` and `problem2_DML.sql` (library database).
2. Copy `website/.env.example` to `website/.env` and set your SQL Server values.
3. Inside the `website` folder run:

        pip install -r requirements.txt
        python app.py

4. Open http://127.0.0.1:5000 (To-Do) or http://127.0.0.1:5000/library (Library).
