import re
import psycopg2

# Database connection details
db_host = 'localhost'
db_name = 'konark'
db_user = 'postgres'
db_password = 't@rHB123'

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=db_host,
    database=db_name,
    user=db_user,
    password=db_password
)
cursor = conn.cursor()

# Regular expression for log line parsing
log_regex = re.compile(r'^(\S+)\s+-\s+-\s+\[(.*?)\]\s+"(\S+)\s+(\S+)\s+HTTP/\d\.\d"\s+(\d+)\s+(\d+|-)"')

# Log file path
log_file = 'path_to_log_file'

# Function to insert log entries into the database
def insert_log_entry(log_entry):
    query = "INSERT INTO apache_logs (remote_host, timestamp, request_method, requested_url, http_status_code, bytes_transferred) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, log_entry)

# Read and parse log file
with open(log_file, 'r') as file:
    for line in file:
        match = log_regex.match(line)
        if match:
            log_entry = match.groups()
            insert_log_entry(log_entry)

# Commit the changes and close the database connection
conn.commit()
conn.close()
