import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%notification%';")
tables = cursor.fetchall()

print("Notification-related tables:")
for table in tables:
    print(f"  - {table[0]}")

cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='notifications_notificationpreference';")
result = cursor.fetchone()

if result:
    print(f"\n✓ Table 'notifications_notificationpreference' exists!")

    cursor.execute("PRAGMA table_info(notifications_notificationpreference);")
    columns = cursor.fetchall()
    
    print("\nTable schema:")
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
else:
    print("\n✗ Table 'notifications_notificationpreference' does not exist.")

conn.close()
