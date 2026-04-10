# Bookstore Management System

## Team Members
- Jeremy N - Scrum Master
- Danielle N - QA tester
- Kyle W - QA tester
- Aeryn W - Developer

## Project Overview
This project is a desktop Bookstore Management System built with Python and Tkinter. It includes a login screen, dashboard, inventory management workflow, customer management, order placement, and JSON-based local persistence.

## Features
- Validate login input
- View a dashboard with inventory summary metrics
- Browse current inventory in a table
- Open a single book record to review its details
- Search inventory by title, author, and ISBN
- Add, edit, and delete books with validation
- Manage customers and place orders
- View sales history, sale details, and date-based filters
- Let logged-in customers place orders and view order statuses
- Persist books, customers, and orders to local JSON storage
- Track inventory totals and estimated stock value

## Tech Stack
- Python
- Tkinter
- Git/GitHub

## Run The App
```bash
python3 src/main.py
```

## Run Tests
```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

## Data Storage
- App data is saved to `data/bookstore_data.json`
- On first launch, the app seeds sample books automatically

## Repository Workflow
1. Pull latest changes from `main`
2. Create a feature branch
3. Make changes
4. Commit and push branch
5. Open a pull request
6. Get review before merging

## Folder Structure
- `docs/` project documentation
- `src/` application source code
- `tests/` unit tests
- `assets/` screenshots and diagrams
