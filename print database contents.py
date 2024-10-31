import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('student_discounts.db')
cursor = conn.cursor()

# Retrieve all entries from the discounts table
cursor.execute('SELECT * FROM govt_scholarships')
rows = cursor.fetchall()

# Print the contents of the database
for row in rows:
    print(f"ID: {row[0]}")
    print(f"Source: {row[1]}")
    print(f"Company: {row[2]}")
    print(f"Logo: {row[3]}")
    print(f"Discount: {row[4]}")

    print("-----")

# Close the database connection
conn.close()
