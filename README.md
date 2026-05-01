# Secure Student Management System

Python II course final project for managing student records, user accounts, grades, reports, and grade visualizations from a command-line interface.

## Group Members

- Ben Toebben
- Caleb Mitchell
- Eric Beltran
- Jace Rushing

## Project Overview

This application lets users register and log in, then routes them to either a regular user dashboard or an admin dashboard. Regular users can view the student record linked to their account. Admin users can create and manage student records, link records to user accounts, manage user roles, enter grades, export CSV reports, and view grade charts.

The project can run through a remote API server by default, while the API server itself talks to DynamoDB. The shared data access code in `data_handler.py` keeps the rest of the project from needing to know whether it is using the remote API or direct DynamoDB access.

## Current Features

- Command-line registration and login
- Password hashing with a salt
- User roles for regular users and admins
- Admin creation, editing, viewing, and deletion of student records
- Admin deletion of user accounts
- Admin role promotion and revocation
- Admin linking of user accounts to student profiles
- Regular user viewing of their linked student record
- Grade entry and average calculation
- CSV export for student rosters and report cards
- Grade visualization with Matplotlib
- API client/server path for remote data access

## Main Files

- `main.py`: Starts the CLI application and checks the remote API connection.
- `menu.py`: Contains the command-line menus and user/admin workflows.
- `user.py`: Defines user classes and login/registration logic.
- `student.py`: Defines the student record model.
- `data_handler.py`: Handles user and student persistence through the API or DynamoDB.
- `api.py`: Runs the HTTP API server.
- `api_client.py`: Sends requests from the CLI to the API server.
- `grade_manager.py`: Calculates averages and updates grade lists.
- `analytics.py`: Displays grade graphs with Matplotlib.
- `reports.py`: Exports CSV report files.
- `validator.py`: Validates names, emails, phone numbers, and passwords.
- `security.py`: Hashes passwords with salts.
- `session_manager.py`: Tracks the currently logged-in user.

## Requirements

Install the project dependencies with:

```bash
pip install -r requirements.txt
```

The main third-party libraries are:

- `boto3`
- `matplotlib`

The project also uses standard Python libraries including `csv`, `datetime`, `hashlib`, `hmac`, `json`, `os`, `random`, `re`, and `urllib`.

## Running the CLI

Run the command-line application with:

```bash
python main.py
```

By default, `main.py` uses the remote API configured in `api_client.py`.

## Running the API Server

Run the local API server with:

```bash
python api.py
```

Optional environment variables:

- `HOST`: API bind host. Defaults to `0.0.0.0`.
- `PORT`: API port. Defaults to `5000`.
- `API_SECRET`: Secret used to sign login tokens.
- `AWS_REGION`: DynamoDB region. Defaults to `us-east-2`.

## Notes

- New user registration creates only a user account. Student profiles are created and linked from the admin menu.
- Student IDs are generated automatically.
- Regular users must have a linked `student_id` before they can view a student record.
- CSV exports are written to the project folder as `student_roster.csv` and `report_cards.csv`.
