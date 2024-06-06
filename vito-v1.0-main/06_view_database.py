import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('customer_faces_data.db')
c = conn.cursor()

# Query the database
c.execute("SELECT * FROM customers")
rows = c.fetchall()

# Display the data
print("Database content:")
for row in rows:
    print(f"ID: {row[0]}, Customer UID: {row[1]}, Customer Name: {row[2]}, Image Path: {row[3]}")

# Close the database connection
conn.close()
