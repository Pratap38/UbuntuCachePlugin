# #!/bin/bash

# set -e

# echo "======================================="
# echo " Ubuntu Cache Cleaner Uninstaller"
# echo "======================================="
# echo ""

# echo "Removing Ubuntu Cache Cleaner..."

# python3 -m pip uninstall Baker -y

# echo ""
# echo "Removing build files..."

# rm -rf build
# rm -rf dist
# rm -rf *.egg-info
# rm -f cacheclean.spec

# echo ""
# echo "Uninstallation Completed Successfully."

# echo "======================================="



#!/bin/bash

set -e

echo "======================================="
echo " Ubuntu Cache Cleaner Uninstaller"
echo "======================================="
echo ""

echo "Stopping RAM Guardian..."

systemctl --user stop ubuntu-cache-cleaner-guardian.service || true

echo ""
echo "Disabling RAM Guardian..."

systemctl --user disable ubuntu-cache-cleaner-guardian.service || true

echo ""
echo "Removing RAM Guardian service..."

SYSTEMD_USER_DIR="$HOME/.config/systemd/user"

rm -f "$SYSTEMD_USER_DIR/ubuntu-cache-cleaner-guardian.service"

systemctl --user daemon-reload || true

echo ""
echo "Removing RAM Guardian runtime files..."

rm -rf "$HOME/.config/ubuntu-cache-cleaner"
rm -rf "$HOME/.local/state/ubuntu-cache-cleaner"

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