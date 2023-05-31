import re
import psycopg2

# Database connection details
db_host = 'localhost'
db_name = 'konark'
db_user = 'postgres'
db_password = 't@rHB123'

# Connect to the PostgreSQL database
try:
    conn = psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password
    )
    cursor = conn.cursor()
except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL:", error)
    exit()

# Regular expressions for log line parsing
apache_log_regex = re.compile(r'^(\S+)\s+\S+\s+(\S+)\s+\[(.*?)\]\s+"(\S+)\s+(\S+)\s+HTTP/\d\.\d"\s+(\d+)\s+(\d+)\s+"([^"]+)"')
exim4_log_regex = re.compile(r'^(\S+)\s+\S+\s+(\S+)\s+<([^>]+)>\s+.*\s+id=.*\s+(.*):\s+(.*);\s+(.*)')

# Log file paths
apache_log_file = r'insert path here'
exim4_log_file = r'insert path here'

# Function to insert Apache log entries into the database
def insert_apache_log_entry(log_entry):
    query = "INSERT INTO apache_logs (remote_host, timestamp, request_method, requested_url, http_status_code, bytes_transferred, user_agent) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    try:
        cursor.execute(query, log_entry)
    except (Exception, psycopg2.Error) as error:
        print("Error while inserting Apache log entry:", error)
        raise

# Function to insert Exim4 log entries into the database
def insert_exim4_log_entry(log_entry):
    query = "INSERT INTO exim4_logs (timestamp, sender, recipient, message, status, error_message) VALUES (%s, %s, %s, %s, %s, %s)"
    try:
        cursor.execute(query, log_entry)
    except (Exception, psycopg2.Error) as error:
        print("Error while inserting Exim4 log entry:", error)
        raise

# Read and parse Apache log file
try:
    with open(apache_log_file, 'r') as file:
        for line in file:
            match = apache_log_regex.match(line)
            if match:
                log_entry = match.groups()
                insert_apache_log_entry(log_entry)
except FileNotFoundError as error:
    print("Error while reading Apache log file:", error)
    exit()

# Read and parse Exim4 log file
try:
    with open(exim4_log_file, 'r') as file:
        for line in file:
            match = exim4_log_regex.match(line)
            if match:
                log_entry = match.groups()
                insert_exim4_log_entry(log_entry)
except FileNotFoundError as error:
    print("Error while reading Exim4 log file:", error)
    exit()

# Commit the changes and close the database connection
try:
    conn.commit()
    print("Log entries inserted into the database.")
except (Exception, psycopg2.Error) as error:
    print("Error while committing changes to the database:", error)
# The result of executing this code is
# lilyi/OneDrive/Documents/GitHub/bharatc12.github.io/ingest script.py"
# Log entries inserted into the database.
conn.close()

