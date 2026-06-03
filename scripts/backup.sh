#!/bin/bash

date=$(date +%Y-%m-%d_%H-%M)

mkdir -p backups

zip -r "backups/backup_$date.zip" . \
    --exclude "venv/*" \
    --exclude ".git/*" \
    --exclude "*__pycache__/*" \
    --exclude "backups/*" \
    --exclude "scripts/*" \
    --exclude ".env" \
    --exclude ".gitignore" \
    --exclude "discloud.config" \
    --exclude "requirements.txt"

echo "Backup criado: backup_$date.zip"