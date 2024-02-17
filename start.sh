#!/bin/bash


echo "Starting the server"
xterm -e "python3 ./server.py" &

echo "Starting the AI service"
xterm -e "python3 ./predictor.py" &
