import sqlite3

# Connect to the database
conn = sqlite3.connect('./instance/class.db')
cursor = conn.cursor()

# Update the attendance value for each student
cursor.execute("UPDATE Student SET attendance = ?", (False,))

# Commit the changes and close the connection
conn.commit()
conn.close()
