# reset_db.py
"""
Script to reset the SQLite database used by the application.
It deletes the existing database file (if any) and recreates all tables
using the SQLAlchemy models defined in the project.
"""
import os
import sys

# Ensure the project root is in the Python path
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

from website import create_app, db

def reset_database():
    app = create_app()
    # Path to the SQLite database file (as used in config)
    db_path = os.path.join(project_root, "instance", "blog.db")
    # Remove the database file if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Deleted existing database at {db_path}")
    else:
        print("No existing database file found; proceeding to create a fresh one.")

    # Recreate all tables
    with app.app_context():
        db.create_all()
        print("Database tables recreated successfully.")

if __name__ == "__main__":
    reset_database()
