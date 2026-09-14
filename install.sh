# #!/bin/bash

# echo "======================================="
# echo " Ubuntu Cache Cleaner Installer"
# echo "======================================="
# echo ""

# echo "Checking Python..."

# python3 --version

# echo ""
# echo "Installing Python Dependencies..."

# python3 -m pip install -r requirements.txt

# echo ""
# echo "Installing Ubuntu Cache Cleaner..."

# python3 -m pip install -e .

# echo ""
# echo "Installation Successful!"
# echo ""

# echo "Run the application using:"
# echo ""

# echo "cacheclean"

# echo ""
# echo "======================================="



#!/bin/bash

set -e

echo "======================================="
echo " Ubuntu Cache Cleaner Installer"
echo "======================================="
echo ""

echo "Installing dependencies..."
python3 -m pip install -r requirements.txt

echo ""
echo "Installing Ubuntu Cache Cleaner..."
python3 -m pip install -e .

echo ""
echo "Installing RAM Guardian service..."

SYSTEMD_USER_DIR="$HOME/.config/systemd/user"

mkdir -p "$SYSTEMD_USER_DIR"

cp systemd/ubuntu-cache-cleaner-guardian.service \
   "$SYSTEMD_USER_DIR/ubuntu-cache-cleaner-guardian.service"

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