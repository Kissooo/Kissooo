import sqlite3

# Connect to the database (it will be created if it doesn't exist)
connection = sqlite3.connect('database.db')

# Create a cursor object to execute SQL commands
cursor = connection.cursor()

# SQL command to create the 'items' table
# Using IF NOT EXISTS to prevent errors if the script is run multiple times
create_table_query = """
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    code TEXT UNIQUE NOT NULL,
    purchase_date TEXT NOT NULL,
    price REAL NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# Execute the command
cursor.execute(create_table_query)

print("Table 'items' created successfully (if it didn't exist).")

# Check if the table is empty before inserting sample data
cursor.execute("SELECT COUNT(id) FROM items")
item_count = cursor.fetchone()[0]

if item_count == 0:
    print("Table is empty. Inserting sample data...")
    # Insert some sample data
    sample_data = [
        ('เก้าอี้สำนักงาน', 'OFF-CHR-001', '2023-01-15', 1500.00, 'ใช้งานอยู่'),
        ('โต๊ะทำงาน', 'OFF-DSK-001', '2023-01-15', 3500.50, 'ใช้งานอยู่'),
        ('คอมพิวเตอร์ Dell', 'IT-PC-015', '2024-02-20', 25000.00, 'ว่าง')
    ]
    cursor.executemany("INSERT INTO items (name, code, purchase_date, price, status) VALUES (?, ?, ?, ?, ?)", sample_data)
    print("Sample data inserted.")
else:
    print("Table already contains data. Skipping sample data insertion.")


# Commit the changes and close the connection
connection.commit()
connection.close()

print("Database initialized successfully.")
