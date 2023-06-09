#!/usr/bin/env python

#built in moudule to python
import sys
#Module used to connect to postgres databases
import psycopg2 

# Connect to the PostgreSQL database
db = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="t@rHB123",
    database="emails"
)

# Obtain the necessary information from the command line arguments
mail_from = sys.argv[1]
rcpt_to = sys.argv[2]
body = sys.stdin.read()

# Insert the email into the database
cursor = db.cursor()
query = "INSERT INTO emails (sender, recipient, body) VALUES (%s, %s, %s)"
values = (mail_from, rcpt_to, body)
cursor.execute(query, values)
db.commit()

# Close the database connection
db.close()
