import sys
import email
import psycopg2
from email.utils import parseaddr
from datetime import datetime

# Function to parse the email and extract relevant data
def parse_email(message_text):
    msg = email.message_from_string(message_text)
    from_email = parseaddr(msg['From'])[1]
    sender = parseaddr(msg['Sender'])[1] if 'Sender' in msg else None
    to_email = parseaddr(msg['To'])[1]
    envelope_to = parseaddr(msg['X-Envelope-To'])[1] if 'X-Envelope-To' in msg else None
    transmission_time = datetime.now()
    transmitting_smtp_server = msg['X-Exim-Transmitting-SMTP-Server']
    subject = msg['Subject']
    body = msg.get_payload()

    return (from_email, sender, to_email, envelope_to, transmission_time, transmitting_smtp_server, subject, body)

# Function to insert data into PostgreSQL database
def insert_into_database(data):
    connection = psycopg2.connect(
        host="",
        database="",
        user="",
        password=""
    )
    cursor = connection.cursor()

    query = """
        INSERT INTO email_message (from_email, sender, to_email, envelope_to, transmission_time, transmitting_smtp_server, subject, body)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(query, data)
    connection.commit()
    cursor.close()
    connection.close()

# Read the email message from stdin
message_text = sys.stdin.read()

# Parse the email and extract data
data = parse_email(message_text)

# Insert the data into the PostgreSQL database
insert_into_database(data)
