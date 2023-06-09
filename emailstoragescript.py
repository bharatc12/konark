#!/usr/bin/env python

#built in module to python
import sys
#module used to connect to postgres
import psycopg2

#Connect to the PostgreSQL database
db = psycopg2.connect(
host="localhost",
user="your_username",
password="your_password",
database="your_database"
)

#Obtain the necessary information from the script arguments
mail_from = sys.argv[1]
rcpt_to = sys.argv[2]
body = sys.stdin.read()

#Check if the email is a relay email
is_relay = False
if "@" in mail_from and "@" in rcpt_to:
mail_from_domain = mail_from.split("@")[1]
rcpt_to_domain = rcpt_to.split("@")[1]
if mail_from_domain == rcpt_to_domain:
is_relay = True

#Insert the email into the database if it is not a relay email
if not is_relay:
cursor = db.cursor()
query = "INSERT INTO email_logs (mail_from, rcpt_to, body) VALUES (%s, %s, %s)"
values = (mail_from, rcpt_to, body)
cursor.execute(query, values)
db.commit()

#Close the database connection
db.close()

#to run this script
#using the following command python emailstoragescript.py <mail_from_address> <rcpt_to_address>
