import sqlite3
import os

def migrate():
    db_path = 'instance/blog.db'
    if not os.path.exists(db_path):
        print("No database found.")
        return

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    columns = [
        ("asin", "VARCHAR(20)"),
        ("product_title", "VARCHAR(255)"),
        ("current_price", "FLOAT"),
        ("original_price", "FLOAT"),
        ("discount_percentage", "INTEGER"),
        ("is_available", "BOOLEAN DEFAULT 1"),
        ("last_synced_at", "DATETIME")
    ]
    
    for col_name, col_type in columns:
        try:
            c.execute(f"ALTER TABLE affiliate_link ADD COLUMN {col_name} {col_type}")
            print(f"Added {col_name} to affiliate_link table.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print(f"Column {col_name} already exists.")
            else:
                print(f"Error adding {col_name}: {e}")

    conn.commit()
    conn.close()
    print("Migration complete.")

if __name__ == "__main__":
    migrate()
