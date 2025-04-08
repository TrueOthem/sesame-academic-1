import psycopg2

try:
    conn = psycopg2.connect("dbname=sesame")
    print("Connected to the database successfully!")
    
    # Create a cursor
    cur = conn.cursor()
    
    # Execute a query
    cur.execute("SELECT * FROM users LIMIT 5")
    
    # Fetch the results
    rows = cur.fetchall()
    print(f"Found {len(rows)} users")
    
    # Close the cursor and connection
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"Error connecting to the database: {e}")
