#!/bin/bash

#use this command chmod +x firewall.sh
#and this command./block_port_scanner.sh (insert ip)

# Define the threshold for port scanning detection
THRESHOLD=10

# Get the source IP address from the command line argument
IP_ADDRESS=$1

# Check if the IP address is already blocked
if iptables -L INPUT -v -n | grep -q "$IP_ADDRESS"; then
  echo "IP address $IP_ADDRESS is already blocked."
  exit 0
fi

# Get the count of open ports for the given IP address
PORT_COUNT=$(nmap -p- -Pn "$IP_ADDRESS" | grep "open" | wc -l)

# Check if the port count exceeds the threshold
if [ "$PORT_COUNT" -ge "$THRESHOLD" ]; then
  echo "Port scanning detected from IP address $IP_ADDRESS. Blocking..."
  iptables -A INPUT -s "$IP_ADDRESS" -j DROP
  echo "IP address $IP_ADDRESS is blocked."
else
  echo "No port scanning detected from IP address $IP_ADDRESS."
fi
