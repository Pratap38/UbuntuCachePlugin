#!/bin/bash

set -euo pipefail

EXT_UUID="ram-guardian-focus@ubuntu-cache-cleaner"
EXT_SOURCE_DIR="gnome-extension/ram-guardian-focus"
PRIMARY_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
FALLBACK_DATA_HOME="$HOME/.local/share"

if mkdir -p "$PRIMARY_DATA_HOME" 2>/dev/null && [ -w "$PRIMARY_DATA_HOME" ]; then
    DATA_HOME="$PRIMARY_DATA_HOME"
else
    DATA_HOME="$FALLBACK_DATA_HOME"
fi

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
echo "If this shell session uses a non-standard XDG_DATA_HOME, install the extension"
echo "from the same environment where GNOME Shell is running."
