#!/bin/bash

echo "======================================="
echo " Ubuntu Cache Cleaner Installer"
echo "======================================="
echo ""

echo "Checking Python..."

python3 --version

echo ""
echo "Installing Python Dependencies..."

python3 -m pip install -r requirements.txt

echo ""
echo "Installing Ubuntu Cache Cleaner..."

python3 -m pip install -e .

echo ""
echo "Installation Successful!"
echo ""

echo "Run the application using:"
echo ""

echo "cacheclean"

echo ""
echo "======================================="