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

# Regular expressions for log line parsing
apache_log_regex = re.compile(r'^(\S+)\s+\S+\s+(\S+)\s+\[(.*?)\]\s+"(\S+)\s+(\S+)\s+HTTP/\d\.\d"\s+(\d+)\s+(\d+)\s+"([^"]+)"')
exim4_log_regex = re.compile(r'^(\S+)\s+\S+\s+(\S+)\s+<([^>]+)>\s+.*\s+id=.*\s+(.*):\s+(.*);\s+(.*)')

# Log file paths
apache_log_file = 'path_to_apache_log_file'
exim4_log_file = 'path_to_exim4_log_file'

# Function to insert Apache log entries into the database
def insert_apache_log_entry(log_entry):
    query = "INSERT INTO apache_logs (remote_host, timestamp, request_method, requested_url, http_status_code, bytes_transferred, user_agent) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, log_entry)

# Function to insert Exim4 log entries into the database
def insert_exim4_log_entry(log_entry):
    query = "INSERT INTO exim4_logs (timestamp, sender, recipient, message, status, error_message) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, log_entry)

# Read and parse Apache log file
with open(apache_log_file, 'r') as file:
    for line in file:
        match = apache_log_regex.match(line)
        if match:
            log_entry = match.groups()
            insert_apache_log_entry(log_entry)

# Read and parse Exim4 log file
with open(exim4_log_file, 'r') as file:
    for line in file:
        match = exim4_log_regex.match(line)
        if match:
            log_entry = match.groups()
            insert_exim4_log_entry(log_entry)

# Commit the changes and close the database connection
conn.commit()
conn.close()
