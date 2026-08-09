#!/bin/bash

set -euo pipefail

EXT_UUID="ram-guardian-focus@ubuntu-cache-cleaner"
EXT_SOURCE_DIR="gnome-extension/ram-guardian-focus"

# GNOME Shell itself runs with no XDG_DATA_HOME override and always reads
# extensions from $HOME/.local/share/gnome-shell/extensions. Do NOT honor
# XDG_DATA_HOME from the invoking shell here: terminals launched from snap
# packages (e.g. VS Code's integrated terminal) rewrite XDG_DATA_HOME to a
# private snap sandbox path, which silently installs the extension where
# GNOME Shell will never see it.
DATA_HOME="$HOME/.local/share"

EXT_TARGET_DIR="$DATA_HOME/gnome-shell/extensions/$EXT_UUID"

echo "Installing RAM Guardian GNOME Shell extension..."
echo "Target: $EXT_TARGET_DIR"

if [ ! -d "$EXT_SOURCE_DIR" ]; then
    echo "Source directory not found: $EXT_SOURCE_DIR" >&2
    exit 1
fi

if [ ! -f "$EXT_SOURCE_DIR/metadata.json" ] || [ ! -f "$EXT_SOURCE_DIR/extension.js" ]; then
    echo "Missing metadata.json or extension.js in $EXT_SOURCE_DIR" >&2
    exit 1
fi

mkdir -p "$EXT_TARGET_DIR"
cp "$EXT_SOURCE_DIR/metadata.json" "$EXT_TARGET_DIR/"
cp "$EXT_SOURCE_DIR/extension.js" "$EXT_TARGET_DIR/"

if ! grep -q "\"uuid\": \"$EXT_UUID\"" "$EXT_TARGET_DIR/metadata.json"; then
    echo "UUID mismatch after install" >&2
    exit 1
fi

echo "Installed files:"
ls -la "$EXT_TARGET_DIR"

echo
echo "Discovery check:"
if gnome-extensions list 2>/dev/null | grep -Fq "$EXT_UUID"; then
    echo "GNOME discovery: found"
else
    echo "GNOME discovery: not reported by gnome-extensions list in this session"
fi

echo
echo "After installing, reload the extension:"
echo "  gnome-extensions disable $EXT_UUID && gnome-extensions enable $EXT_UUID"
echo "If GNOME Shell still runs the old code (GNOME 45+ caches the JS module"
echo "on Wayland), log out and back in to fully restart the shell."
