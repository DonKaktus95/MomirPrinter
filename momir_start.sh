#!/bin/bash

echo "Activating virtual environment and starting Momir Printer..."
# Go to script directory
cd <path to dir where momir.py is>
# Open venv
activate() {
    . <path to the activate file for used virtual env>
}
activate
# Start the app
python3 <full path to momir.py>