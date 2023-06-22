import psycopg2
import re
from datetime import datetime

# Define database connection details
db_host = "your_database_host"
db_name = "your_database_name"
db_user = "your_username"
db_password = "your_password"

# Connect to the database
conn = psycopg2.connect(
    host=db_host,
    database=db_name,
    user=db_user,
    password=db_password
)

# Function to insert data into syslog table
def insert_syslog_entry(entry):
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO syslog (timestamp, hostname, tag, content)
        VALUES (%s, %s, %s, %s)
        """,
        (entry["timestamp"], entry["hostname"], entry["tag"], entry["content"])
    )
    conn.commit()
    cursor.close()

# Function to insert data into auth_log table
def insert_auth_log_entry(entry):
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO auth_log (timestamp, hostname, process, content)
        VALUES (%s, %s, %s, %s)
        """,
        (entry["timestamp"], entry["hostname"], entry["process"], entry["content"])
    )
    conn.commit()
    cursor.close()

# Function to insert data into kern_log table
def insert_kern_log_entry(entry):
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO kern_log (timestamp, hostname, facility, message)
        VALUES (%s, %s, %s, %s)
        """,
        (entry["timestamp"], entry["hostname"], entry["facility"], entry["message"])
    )
    conn.commit()
    cursor.close()

# Function to insert data into daemon_logs table
def insert_daemon_log_entry(entry):
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO daemon_logs (timestamp, hostname, daemon_name, message)
        VALUES (%s, %s, %s, %s)
        """,
        (entry["timestamp"], entry["hostname"], entry["daemon_name"], entry["message"])
    )
    conn.commit()
    cursor.close()


# Function to insert data into dpkg_log table
def insert_dpkg_log_entry(entry):
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO dpkg_log (timestamp, action, package_name, version, architecture, result)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (entry["timestamp"], entry["action"], entry["package_name"], entry["version"], entry["architecture"], entry["result"])
    )
    conn.commit()
    cursor.close()

# Read syslog file and insert entries into syslog table
syslog_file = "/var/log/syslog"
with open(syslog_file, "r") as file:
    for line in file:
        # Parse the log entry and extract relevant fields
        # Adjust the regular expression pattern based on the syslog format in your system
        pattern = r'(\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})\s(\S+)\s(\S+):\s(.*)'
        match = re.match(pattern, line)
        if match:
            entry = {
                "timestamp": datetime.strptime(match.group(1), "%b %d %H:%M:%S"),
                "hostname": match.group(2),
                "tag": match.group(3),
                "content": match.group(4)
            }
            insert_syslog_entry(entry)

# Read auth.log file and insert entries into auth_log table
auth_log_file = "/var/log/auth.log"
with open(auth_log_file, "r") as file:
    for line in file:
        # Parse the log entry and extract relevant fields
        # Adjust the regular expression pattern based on the auth.log format in your system
        pattern = r'(\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})\s(\S+)\s(\S+):\s(.*)'
        match = re.match(pattern, line)
        if match:
            entry = {
                "timestamp": datetime.strptime(match.group(1), "%b %d %H:%M:%S"),
                "hostname": match.group(2),
                "process": match.group(3),
                "content": match.group(4)
            }
            insert_auth_log_entry(entry)

# Read kern.log file and insert entries into kern_log table
kern_log_file = "/var/log/kern.log"
with open(kern_log_file, "r") as file:
    for line in file:
        # Parse the log entry and extract relevant fields
        # Adjust the regular expression pattern based on the kern.log format in your system
        pattern = r'(\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})\s(\S+)\s(\S+):\s(.*)'
        match = re.match(pattern, line)
        if match:
            entry = {
                "timestamp": datetime.strptime(match.group(1), "%b %d %H:%M:%S"),
                "hostname": match.group(2),
                "facility": match.group(3),
                "message": match.group(4)
            }
            insert_kern_log_entry(entry)

# Read daemon.log file and insert entries into daemon_logs table
daemon_log_file = "/var/log/daemon.log"
with open(daemon_log_file, "r") as file:
    for line in file:
        # Parse the log entry and extract relevant fields
        # Adjust the regular expression pattern based on the daemon.log format in your system
        pattern = r'(\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})\s(\S+)\s(\S+):\s(.*)'
        match = re.match(pattern, line)
        if match:
            entry = {
                "timestamp": datetime.strptime(match.group(1), "%b %d %H:%M:%S"),
                "hostname": match.group(2),
                "daemon_name": match.group(3),
                "message": match.group(4)
            }
            insert_daemon_log_entry(entry)

# Read dpkg.log file and insert entries into dpkg_log table
dpkg_log_file = "/var/log/dpkg.log"
with open(dpkg_log_file, "r") as file:
    for line in file:
        # Parse the log entry and extract relevant fields
        # Adjust the regular expression pattern based on the dpkg.log format in your system
        pattern = r'(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s(\S+)\s(\S+)\s(\S+)\s(\S+)\s(\S+)'
        match = re.match(pattern, line)
        if match:
            entry = {
                "timestamp": datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S"),
                "action": match.group(2),
                "package_name": match.group(3),
                "version": match.group(4),
                "architecture": match.group(5),
                "result": match.group(6)
            }
            insert_dpkg_log_entry(entry)

# Close the database connection
conn.close()
