#!/bin/bash

# Vérifiez si un ou deux arguments ont été passés
if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
    echo "Verwendung : ./prepare.sh <Pfad> [resize]"
    echo "  <Pfad> : Verzeichnis mit den Bildern"
    echo "  [resize] : true (standardmäßig) oder false, gibt an, ob die Größe von Bildern geändert werden soll"
    exit 1
fi

# Argumente abrufen
INPUT_DIRECTORY=$1
RESIZE=${2:-true}  # standardmäßig  : true

# Ausführung
python3 prepare.py "$INPUT_DIRECTORY" "$RESIZE"

