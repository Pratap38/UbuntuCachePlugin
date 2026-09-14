#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"

echo "======================================="
echo " Ubuntu Cache Cleaner Installer"
echo "======================================="
echo ""

cd "$PROJECT_ROOT"

echo "Installing dependencies..."
python3 -m pip install -r requirements.txt

echo ""
echo "Installing Ubuntu Cache Cleaner..."
python3 -m pip install -e .

PYTHON_EXECUTABLE="$(python3 -c "import sys; print(sys.executable)")"

echo ""
echo "Installing RAM Guardian service..."

SYSTEMD_USER_DIR="$HOME/.config/systemd/user"

mkdir -p "$SYSTEMD_USER_DIR"

sed \
    -e "s|@PROJECT_ROOT@|$PROJECT_ROOT|g" \
    -e "s|@PYTHON_EXECUTABLE@|$PYTHON_EXECUTABLE|g" \
    "$PROJECT_ROOT/systemd/ubuntu-cache-cleaner-guardian.service" \
    > "$SYSTEMD_USER_DIR/ubuntu-cache-cleaner-guardian.service"

systemctl --user daemon-reload

systemctl --user enable ubuntu-cache-cleaner-guardian.service

systemctl --user start ubuntu-cache-cleaner-guardian.service

echo ""
echo "RAM Guardian installed and started successfully."

echo ""
echo "Installation Completed Successfully."
echo ""
echo "Run the application with:"
echo "cacheclean"
