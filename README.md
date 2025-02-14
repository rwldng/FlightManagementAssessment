# Flight Management System  

A simple command-line tool for managing flights, pilots, and destinations using Python and SQLite for the University of Bath Databases module as part of their MSc Computer Science course

## Contents  
- [What it does](#-what-it-does)  
- [How to set it up](#-how-to-set-it-up)  
- [How it works](#-how-it-works)  
- [Project files](#-project-files)  
- [Future ideas](#-future-ideas)  

## What it does  
- Add, update, and delete flights 
- Assign pilots (without double-booking them)  
- Search flights by destination, status, or departure time
- Keeps data clean and organized with smart constraints

## How to set it up  
1. Clone the repo
2. Make sure you have Python installed
4. Run the program by running main.py
5. Set up the initial database tables by selecting 1 from the menu
6. Populate the sample data by running sample_data.py
7. Run main.py again and start managing flights!

## How it works
- SQLite stores all the flight data
- Python runs the application and Command Line Interface (CLI)

## Project files  
- [`main.py`](main.py) --> Runs the application and CLI menu  
- [`db_operations.py`](db_operations.py) --> Handles all database interactions (creating tables, queries, updates)  
- [`sample_data.py`](sample_data.py) --> Populates the database with sample flights, pilots, and destinations  
- [`queries.py`](queries.py) --> Contains reusable SQL queries  
- [`menu.py`](menu.py) --> Handles user input and navigation in the CLI  

## Future ideas
- A fancy GUI instead of the CLI
- Auto-assigning pilots based on their availability when we add new flights
- Security features so only approved users can change flights