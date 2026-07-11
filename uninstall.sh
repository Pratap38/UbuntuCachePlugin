#!/bin/bash

set -e

echo "======================================="
echo " Ubuntu Cache Cleaner Uninstaller"
echo "======================================="
echo ""

echo "Removing Ubuntu Cache Cleaner..."

python3 -m pip uninstall Baker -y

echo ""
echo "Removing build files..."

rm -rf build
rm -rf dist
rm -rf *.egg-info
rm -f cacheclean.spec

echo ""
echo "Uninstallation Completed Successfully."

echo "======================================="