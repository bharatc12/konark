#!/bin/bash

	echo "Content-Type: application/json"
	echo ""

	# Execute the C++ program and capture the output and errors
	result=$(./matrix_multiply 2>&1)

	if [ $? -eq 0 ]; then
    echo "{ \"result\": \"$result\" }"
	else
    echo "{ \"error\": \"Failed to execute matrix_multiply: $result\" }"
	fi
        
		
		
      
