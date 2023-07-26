CREATE TABLE email_message (
    id SERIAL PRIMARY KEY,
    from_email VARCHAR(255) NOT NULL,
    sender VARCHAR(255),
    to_email VARCHAR(255) NOT NULL,
    envelope_to VARCHAR(255),
    transmission_time TIMESTAMP NOT NULL,
    transmitting_smtp_server VARCHAR(255) NOT NULL,
    reception_time TIMESTAMP,
    receiving_smtp_server VARCHAR(255),
    subject VARCHAR(255),
    body TEXT
    
);
