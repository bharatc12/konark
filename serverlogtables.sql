-- Apache Log Schema
CREATE TABLE apache_logs (
    id SERIAL PRIMARY KEY,
    remote_host VARCHAR(255),
    timestamp TIMESTAMP,
    request_method VARCHAR(10),
    requested_url VARCHAR(255),
    http_status_code INT,
    bytes_transferred BIGINT,
    user_agent VARCHAR(255)
);

-- Exim4 Log Schema
CREATE TABLE exim4_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    sender VARCHAR(255),
    recipient VARCHAR(255),
    message VARCHAR(255),
    status VARCHAR(50),
    error_message TEXT
);